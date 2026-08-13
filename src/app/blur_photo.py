import cv2
import os

from .detector import detector
from .anoymizer import getBlurrer, BlurMethod
from .detect_face import detect_face
from .get_embiddings import get_embedding
from .filter_faces import filter_faces_by_frame


OUTPUT_DIR = "/tmp/videos/output"


def blur_photo(
    method: BlurMethod,
    input: str,
    output: str,
):
    blurrer = getBlurrer(method)

    image = cv2.imread(input)

    if image is None:
        raise ValueError(f"Could not read image: {input}")


    faces = detector.detect(image)

    anonymized = blurrer.anonymize(image, faces)

    output_path = os.path.join(OUTPUT_DIR, output)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    success = cv2.imwrite(output_path, anonymized)

    if not success:
        raise RuntimeError(f"Failed to write output image: {output_path}")

    return output_path


def blur_photo_by_target(
    method: BlurMethod,
    input: str,
    output: str,
    target_img: str,
):
    blurrer = getBlurrer(method)

    # Detect the face in the target image
    target_face, target_image = detect_face(
        target_image=target_img
    )

    target_embedding = get_embedding(
        target_face=target_face,
        target_image=target_image,
    )

    image = cv2.imread(input)

    if image is None:
        raise ValueError(f"Could not read image: {input}")

    print("input:", input)
    print("width:", image.shape[1])
    print("height:", image.shape[0])

    # Find only faces matching the target embedding
    filtered_faces = filter_faces_by_frame(
        image=image,
        target_embedding=target_embedding,
    )

    anonymized = blurrer.anonymize(
        image,
        filtered_faces,
    )

    output_path = os.path.join(OUTPUT_DIR, output)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    success = cv2.imwrite(output_path, anonymized)

    if not success:
        raise RuntimeError(f"Failed to write output image: {output_path}")

    return output_path