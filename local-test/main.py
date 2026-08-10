import modal
import os

os.makedirs("/tmp/videos", exist_ok=True)
os.makedirs("/tmp/videos/output", exist_ok=True)

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


if __name__=="__main__":
    blur_video_api(body={
  "key": "256701.mp4",
  "output_key": "string-256701.mp4",
  "blur_method": "pixelate"
})
