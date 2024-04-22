import logging
import os
import sys
import gradio as gr
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import routes
from ..utils import app_helpers, session_logger, utils


session_logger.change_logging(logging.DEBUG)

CUSTOM_GRADIO_PATH = "/"
app = FastAPI(title="lisa_app", version="1.0")
app.include_router(routes.router)

os.makedirs(utils.FASTAPI_STATIC, exist_ok=True)
app.mount("/static", StaticFiles(directory=utils.FASTAPI_STATIC), name="static")
templates = Jinja2Templates(directory="templates")


app_helpers.app_logger.info(f"sys.argv:{sys.argv}.")
args = app_helpers.parse_args([])
app_helpers.app_logger.info(f"prepared default arguments:{args}.")
inference_fn = app_helpers.get_inference_model_by_args(args)
app_helpers.app_logger.info(f"prepared inference_fn function:{inference_fn.__name__}, creating gradio interface...")
io = app_helpers.get_gradio_interface(inference_fn)
app_helpers.app_logger.info("created gradio interface")
app = gr.mount_gradio_app(app, io, path=CUSTOM_GRADIO_PATH)
app_helpers.app_logger.info("mounted gradio app within fastapi")
