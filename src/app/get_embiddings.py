from .recognizer import recognizer
from uniface import Face
def get_embedding(target_face:Face, target_image:str):
    target_embedding = recognizer.get_normalized_embedding(
    target_image,
    target_face.landmarks
)
    return target_embedding