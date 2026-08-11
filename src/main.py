import modal
import os

os.makedirs("/tmp/videos", exist_ok=True)
os.makedirs("/tmp/videos/output", exist_ok=True)

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


@app.function(image=image,secrets=[secrets])
@modal.asgi_app()
def api():
    from fastapi import FastAPI,Request,Depends
    from app.modals  import BlurVideoResponse,BlurVideoRequest,BlurVideoRequestSelective
    from app.blur_video import blur_video,blur_video_by_target
    from app.api_middleware import apiMiddleware
    web_app = FastAPI()
    @web_app.middleware("http")
    async def log_requests(request: Request, call_next):
        print(f"{request.method} {request.url}")

        response = await call_next(request)

        print(f"Status: {response.status_code}")

        return response
    @web_app.get("/")
    def home():
        return {
            "message":"hello world"
        }
        
    @web_app.post("/api/blur-video",dependencies=[Depends(apiMiddleware)])
    def  blur_video_api(body:BlurVideoRequest):
        from app.s3 import download_video,upload_video
        try:
            file_path = download_video(body.key)
            print(file_path)
            output = blur_video(method=body.blur_method, output=body.output_key, input=file_path)
            upload_video(body.output_key, output)
            return {"success":True, "key":body.output_key}
        except Exception as e :
            print(e)
            return {"success":False}
    @web_app.post("/api/blur-video/selective",dependencies=[Depends(apiMiddleware)])
    def  blur_video_api(body:BlurVideoRequestSelective):
        from app.s3 import download_video,upload_video
        from app.recover_audio import recover_audio
        try:
            file_path = download_video(body.key)
            target_file_path = download_video(body.target_image)
            output = blur_video_by_target(method=body.blur_method, output=body.output_key, input=file_path, target_img=target_file_path)
            r_video_path = lambda p: (
    os.path.splitext(p)[0] + "_recovered" + os.path.splitext(p)[1]
)
            recovered_video = recover_audio(input=output, output=r_video_path(output),audio_video=file_path)
            upload_video(body.output_key, recovered_video)
            try:
                os.remove(file_path)
                os.remove(target_file_path)
                os.remove(recovered_video)
                os.remove(output)
            except:
                print("Error deleting file")
            return {"success":True, "key":body.output_key}
        except Exception as e :
            print(e)
            return {"success":False}
    return web_app
