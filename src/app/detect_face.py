import cv2

from uniface.detection import RetinaFace
from uniface.recognition import ArcFace
from uniface.draw import draw_detections
from uniface import compute_similarity
from .detector import detector

def detect_face(target_image:str):
    t_image = cv2.imread(target_image)
    if t_image is None:
        raise Exception("Could not load target image")
    target_faces = detector.detect(t_image)
    if not target_faces:
        raise Exception("No target face found")
    target_face = target_faces[0]
    return target_face,t_image