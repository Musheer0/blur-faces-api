from uniface import compute_similarity
from .detector import detector
from .recognizer import recognizer
from numpy import ndarray
def filter_faces(image:str, target_embedding:ndarray):
    faces = detector.detect(image)
    filtered_faces = []
    for face in faces:
        embedding = recognizer.get_normalized_embedding(
        image,
        face.landmarks
    )

        similarity = compute_similarity(
        target_embedding,
        embedding,
        normalized=True
    )

        print("Similarity:", similarity)

    # Keep faces that DON'T match target
        if similarity < 0.4:
            filtered_faces.append(face)
    return filter_faces
def filter_faces_by_frame(
    image: ndarray,
    target_embedding: ndarray,
):
    faces = detector.detect(image)

    filtered_faces = []

    for face in faces:
        embedding = recognizer.get_normalized_embedding(
            image,
            face.landmarks,
        )

        similarity = compute_similarity(
            target_embedding,
            embedding,
            normalized=True,
        )

        # Keep faces that DON'T match target
        if similarity < 0.2:
            filtered_faces.append(face)

    return filtered_faces