import logging
import os

import modal

os.makedirs("/tmp/videos", exist_ok=True)
os.makedirs("/tmp/videos/output", exist_ok=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = modal.App("face-blur-v1")
image = (
    modal.Image.from_registry(
        "nvidia/cuda:13.3.0-cudnn-devel-ubuntu24.04",
        add_python="3.12"
    )
    .apt_install("ffmpeg")
    .pip_install_from_requirements("requirements.txt")
    .add_local_dir("src", remote_path="/root")
)
secrets = modal.Secret.from_name("face-blur")


@app.function(image=image, secrets=[secrets])
@modal.asgi_app()
def api():
    from fastapi import FastAPI

    from app.routes.photo_routes import router as photo_router
    from app.routes.video_routes import router as video_router

    web_app = FastAPI()
    web_app.include_router(video_router)
    web_app.include_router(photo_router)

    @web_app.get("/health")
    def health():
        return {"status": "ok"}

    return web_app
