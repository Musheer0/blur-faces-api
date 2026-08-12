import cv2
from .detector import detector
from .anoymizer import getBlurrer,BlurMethod
from .ffmpeg_writer import FFmpegWriter
from .detect_face import detect_face
from .get_embiddings import get_embedding
from .filter_faces import filter_faces_by_frame
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
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
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
def blur_video_by_target(method:BlurMethod, input: str, output:str, target_img:str):
    blurrer = getBlurrer(method)
    target_face,t_image = detect_face(target_image=target_img)
    target_embedding = get_embedding(target_face=target_face, target_image=t_image)
    
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
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
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
        filtered_faces = filter_faces_by_frame(image=frame, target_embedding=target_embedding)
        anoymized = blurrer.anonymize(frame, filtered_faces)
        output_video.write(anoymized)
    cap.release()
    output_video.release() 
    return output_path
    
