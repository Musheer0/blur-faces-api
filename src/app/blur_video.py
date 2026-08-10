import cv2
from .detector import detector
from .anoymizer import getBlurrer,BlurMethod
from .ffmpeg_writer import FFmpegWriter
import os
def blur_video(method:BlurMethod, input: str, output:str):

    blurrer = getBlurrer(method)
    cap = cv2.VideoCapture(input)
    print("input:", input)
    print("opened:", cap.isOpened())
    print("fps:", cap.get(cv2.CAP_PROP_FPS))
    print("width:", cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    print("height:", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    w =int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    output_path = '/tmp/videos/output/'+output
    os.makedirs("/tmp/videos/output", exist_ok=True)
    output_video = FFmpegWriter(
        output_path,
        w,
        h,
        fps,
        encoder="libx264",
        preset="veryfast",
        crf="18",
    )
    while True:
        ret,frame =cap.read()
        if not ret:
            break
        faces= detector.detect(frame)
        anoymized = blurrer.anonymize(frame, faces)
        output_video.write(anoymized)
    cap.release()
    output_video.release() 
    return output_path
    
    