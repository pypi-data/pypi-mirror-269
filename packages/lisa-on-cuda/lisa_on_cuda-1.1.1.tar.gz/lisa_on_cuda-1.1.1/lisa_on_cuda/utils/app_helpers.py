import argparse
import logging
import os
import re
from typing import Callable
import cv2
import gradio as gr
import nh3
import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, BitsAndBytesConfig, CLIPImageProcessor

from . import constants, session_logger, utils
from lisa_on_cuda.LISA import LISAForCausalLM
from lisa_on_cuda.llava import conversation as conversation_lib
from lisa_on_cuda.llava.mm_utils import tokenizer_image_token
from lisa_on_cuda.segment_anything.utils.transforms import ResizeLongestSide

placeholders = utils.create_placeholder_variables()
app_logger = logging.getLogger(__name__)


@session_logger.set_uuid_logging
def parse_args(args_to_parse, internal_logger=None):
    if internal_logger is None:
        internal_logger = app_logger
    internal_logger.info(f"ROOT_PROJECT:{utils.PROJECT_ROOT_FOLDER}, default vis_output:{utils.VIS_OUTPUT}.")
    parser = argparse.ArgumentParser(description="LISA chat")
    parser.add_argument("--version", default="xinlai/LISA-13B-llama2-v1-explanatory")
    parser.add_argument("--vis_save_path", default=str(utils.VIS_OUTPUT), type=str)
    parser.add_argument(
        "--precision",
        default="fp16",
        type=str,
        choices=["fp32", "bf16", "fp16"],
        help="precision for inference",
    )
    parser.add_argument("--image_size", default=1024, type=int, help="image size")
    parser.add_argument("--model_max_length", default=512, type=int)
    parser.add_argument("--lora_r", default=8, type=int)
    parser.add_argument(
        "--vision-tower", default="openai/clip-vit-large-patch14", type=str
    )
    parser.add_argument("--local-rank", default=0, type=int, help="node rank")
    parser.add_argument("--load_in_8bit", action="store_true", default=False)
    parser.add_argument("--load_in_4bit", action="store_true", default=True)
    parser.add_argument("--use_mm_start_end", action="store_true", default=True)
    parser.add_argument(
        "--conv_type",
        default="llava_v1",
        type=str,
        choices=["llava_v1", "llava_llama_2"],
    )
    return parser.parse_args(args_to_parse)


@session_logger.set_uuid_logging
def get_cleaned_input(input_str, internal_logger=None):
    if internal_logger is None:
        internal_logger = app_logger
    internal_logger.info(f"start cleaning of input_str: {input_str}.")
    input_str = nh3.clean(
        input_str,
        tags={
            "a",
            "abbr",
            "acronym",
            "b",
            "blockquote",
            "code",
            "em",
            "i",
            "li",
            "ol",
            "strong",
            "ul",
        },
        attributes={
            "a": {"href", "title"},
            "abbr": {"title"},
            "acronym": {"title"},
        },
        url_schemes={"http", "https", "mailto"},
        link_rel=None,
    )
    internal_logger.info(f"cleaned input_str: {input_str}.")
    return input_str


@session_logger.set_uuid_logging
def set_image_precision_by_args(input_image, precision):
    if precision == "bf16":
        input_image = input_image.bfloat16()
    elif precision == "fp16":
        input_image = input_image.half()
    else:
        input_image = input_image.float()
    return input_image


@session_logger.set_uuid_logging
def preprocess(
        x,
        pixel_mean=torch.Tensor([123.675, 116.28, 103.53]).view(-1, 1, 1),
        pixel_std=torch.Tensor([58.395, 57.12, 57.375]).view(-1, 1, 1),
        img_size=1024,
) -> torch.Tensor:
    """Normalize pixel values and pad to a square input."""
    logging.info("preprocess started")
    # Normalize colors
    x = (x - pixel_mean) / pixel_std
    # Pad
    h, w = x.shape[-2:]
    padh = img_size - h
    padw = img_size - w
    x = F.pad(x, (0, padw, 0, padh))
    logging.info("preprocess ended")
    return x


@session_logger.set_uuid_logging
def get_model(args_to_parse):
    logging.info("starting model preparation...")
    os.makedirs(args_to_parse.vis_save_path, exist_ok=True)

    # global tokenizer, tokenizer
    # Create model
    _tokenizer = AutoTokenizer.from_pretrained(
        args_to_parse.version,
        cache_dir=None,
        model_max_length=args_to_parse.model_max_length,
        padding_side="right",
        use_fast=False,
    )
    _tokenizer.pad_token = _tokenizer.unk_token
    args_to_parse.seg_token_idx = _tokenizer("[SEG]", add_special_tokens=False).input_ids[0]
    torch_dtype = torch.float32
    if args_to_parse.precision == "bf16":
        torch_dtype = torch.bfloat16
    elif args_to_parse.precision == "fp16":
        torch_dtype = torch.half
    kwargs = {"torch_dtype": torch_dtype}
    if args_to_parse.load_in_4bit:
        kwargs.update(
            {
                "torch_dtype": torch.half,
                "load_in_4bit": True,
                "quantization_config": BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_quant_type="nf4",
                    llm_int8_skip_modules=["visual_model"],
                ),
            }
        )
    elif args_to_parse.load_in_8bit:
        kwargs.update(
            {
                "torch_dtype": torch.half,
                "quantization_config": BitsAndBytesConfig(
                    llm_int8_skip_modules=["visual_model"],
                    load_in_8bit=True,
                ),
            }
        )
    _model = LISAForCausalLM.from_pretrained(
        args_to_parse.version, low_cpu_mem_usage=True, vision_tower=args_to_parse.vision_tower,
        seg_token_idx=args_to_parse.seg_token_idx, **kwargs
    )
    _model.config.eos_token_id = _tokenizer.eos_token_id
    _model.config.bos_token_id = _tokenizer.bos_token_id
    _model.config.pad_token_id = _tokenizer.pad_token_id
    _model.get_model().initialize_vision_modules(_model.get_model().config)
    vision_tower = _model.get_model().get_vision_tower()
    vision_tower.to(dtype=torch_dtype)
    if args_to_parse.precision == "bf16":
        _model = _model.bfloat16().cuda()
    elif (
            args_to_parse.precision == "fp16" and (not args_to_parse.load_in_4bit) and (not args_to_parse.load_in_8bit)
    ):
        vision_tower = _model.get_model().get_vision_tower()
        _model.model.vision_tower = None
        import deepspeed

        model_engine = deepspeed.init_inference(
            model=_model,
            dtype=torch.half,
            replace_with_kernel_inject=True,
            replace_method="auto",
        )
        _model = model_engine.module
        _model.model.vision_tower = vision_tower.half().cuda()
    elif args_to_parse.precision == "fp32":
        _model = _model.float().cuda()
    vision_tower = _model.get_model().get_vision_tower()
    vision_tower.to(device=args_to_parse.local_rank)
    _clip_image_processor = CLIPImageProcessor.from_pretrained(_model.config.vision_tower)
    _transform = ResizeLongestSide(args_to_parse.image_size)
    _model.eval()
    logging.info("model preparation ok!")
    return _model, _clip_image_processor, _tokenizer, _transform


@session_logger.set_uuid_logging
def get_inference_model_by_args(args_to_parse):
    logging.info(f"args_to_parse:{args_to_parse}, creating model...")
    model, clip_image_processor, tokenizer, transform = get_model(args_to_parse)
    logging.info("created model, preparing inference function")
    no_seg_out = placeholders["no_seg_out"]

    @session_logger.set_uuid_logging
    def inference(
            input_str: str,
            input_image: str | np.ndarray,
            internal_logger: logging = None,
            embedding_key: str = None
    ):
        if internal_logger is None:
            internal_logger = app_logger

        # filter out special chars
        input_str = get_cleaned_input(input_str)
        internal_logger.info(f" input_str type: {type(input_str)}, input_image type: {type(input_image)}.")
        internal_logger.info(f"input_str: {input_str}, input_image: {type(input_image)}.")

        # input valid check
        if not re.match(r"^[A-Za-z ,.!?\'\"]+$", input_str) or len(input_str) < 1:
            output_str = f"[Error] Unprocessable Entity input: {input_str}."
            internal_logger.error(output_str)

            from fastapi import status
            from fastapi.responses import JSONResponse

            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"msg": "Error - Unprocessable Entity"}
            )

        # Model Inference
        conv = conversation_lib.conv_templates[args_to_parse.conv_type].copy()
        conv.messages = []

        prompt = utils.DEFAULT_IMAGE_TOKEN + "\n" + input_str
        if args_to_parse.use_mm_start_end:
            replace_token = (
                    utils.DEFAULT_IM_START_TOKEN + utils.DEFAULT_IMAGE_TOKEN + utils.DEFAULT_IM_END_TOKEN
            )
            prompt = prompt.replace(utils.DEFAULT_IMAGE_TOKEN, replace_token)

        conv.append_message(conv.roles[0], prompt)
        conv.append_message(conv.roles[1], "")
        prompt = conv.get_prompt()

        internal_logger.info("read and preprocess image.")
        image_np = input_image
        if isinstance(input_image, str):
            image_np = cv2.imread(input_image)
            image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        original_size_list = [image_np.shape[:2]]
        app_logger.debug("start clip_image_processor.preprocess")
        image_clip = (
            clip_image_processor.preprocess(image_np, return_tensors="pt")[
                "pixel_values"
            ][0]
            .unsqueeze(0)
            .cuda()
        )
        app_logger.debug("done clip_image_processor.preprocess")
        internal_logger.info(f"image_clip type: {type(image_clip)}.")
        image_clip = set_image_precision_by_args(image_clip, args_to_parse.precision)

        image = transform.apply_image(image_np)
        resize_list = [image.shape[:2]]

        internal_logger.debug(f"starting preprocess image: {type(image_clip)}.")
        image = (
            preprocess(torch.from_numpy(image).permute(2, 0, 1).contiguous())
            .unsqueeze(0)
            .cuda()
        )
        internal_logger.info(f"done preprocess image:{type(image)}, image_clip type: {type(image_clip)}.")
        image = set_image_precision_by_args(image, args_to_parse.precision)

        input_ids = tokenizer_image_token(prompt, tokenizer, return_tensors="pt")
        input_ids = input_ids.unsqueeze(0).cuda()

        embedding_key = get_hash_array(embedding_key, image, internal_logger)
        internal_logger.info(f"start model evaluation with embedding_key {embedding_key}.")
        output_ids, pred_masks = model.evaluate(
            image_clip,
            image,
            input_ids,
            resize_list,
            original_size_list,
            max_new_tokens=512,
            tokenizer=tokenizer,
            model_logger=internal_logger,
            embedding_key=embedding_key
        )
        internal_logger.info("model evaluation done, start token decoding...")
        output_ids = output_ids[0][output_ids[0] != utils.IMAGE_TOKEN_INDEX]

        text_output = tokenizer.decode(output_ids, skip_special_tokens=False)
        text_output = text_output.replace("\n", "").replace("  ", " ")
        text_output = text_output.split("ASSISTANT: ")[-1]

        internal_logger.info(
            f"token decoding ended,found n {len(pred_masks)} prediction masks, "
            f"text_output type: {type(text_output)}, text_output: {text_output}."
        )
        output_image = no_seg_out
        output_mask = no_seg_out
        for i, pred_mask in enumerate(pred_masks):
            if pred_mask.shape[0] == 0 or pred_mask.shape[1] == 0:
                continue
            pred_mask = pred_mask.detach().cpu().numpy()[0]
            pred_mask_bool = pred_mask > 0
            output_mask = pred_mask_bool.astype(np.uint8) * 255

            output_image = image_np.copy()
            output_image[pred_mask_bool] = (
                    image_np * 0.5
                    + pred_mask_bool[:, :, None].astype(np.uint8) * np.array([255, 0, 0]) * 0.5
            )[pred_mask_bool]

        output_str = f"ASSISTANT: {text_output} ..."
        internal_logger.info(f"output_image type: {type(output_mask)}.")
        return output_image, output_mask, output_str

    app_logger.info("prepared inference function!")
    return inference


@session_logger.set_uuid_logging
def get_gradio_interface(
        fn_inference: Callable
):
    return gr.Interface(
        fn_inference,
        inputs=[
            gr.Textbox(lines=1, placeholder=None, label="Text Instruction"),
            gr.Image(type="filepath", label="Input Image")
        ],
        outputs=[
            gr.Image(type="pil", label="segmentation Output"),
            gr.Image(type="pil", label="mask Output"),
            gr.Textbox(lines=1, placeholder=None, label="Text Output")
        ],
        title=constants.title,
        description=constants.description,
        article=constants.article,
        examples=constants.examples,
        allow_flagging="auto"
    )


def get_hash_array(embedding_key: str, arr: np.ndarray | torch.Tensor, model_logger: logging):
    from base64 import b64encode
    from hashlib import sha256

    model_logger.debug(f"embedding_key {embedding_key} is None? {embedding_key is None}.")
    if embedding_key is None:
        img2hash = arr
        if isinstance(arr, torch.Tensor):
            model_logger.debug("images variable is a Tensor, start converting back to numpy")
            img2hash = arr.numpy(force=True)
            model_logger.debug("done Tensor converted back to numpy")
        model_logger.debug("start image hashing")
        img2hash_fn = sha256(img2hash)
        embedding_key = b64encode(img2hash_fn.digest())
        embedding_key = embedding_key.decode("utf-8")
        model_logger.debug(f"done image hashing, now embedding_key is {embedding_key}.")
    return embedding_key


if __name__ == '__main__':
    parsed_args = parse_args([])
    print("arrrrg:", parsed_args)
