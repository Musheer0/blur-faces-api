import cv2

from uniface.detection import RetinaFace
from uniface.recognition import ArcFace
from uniface.draw import draw_detections
from uniface import compute_similarity


detector = RetinaFace()
recognizer = ArcFace()

# Target image
target_image = cv2.imread("i.png")

# Frame/image containing faces
image = cv2.imread("s.png")

if target_image is None:
    raise Exception("Could not load target image")

if image is None:
    raise Exception("Could not load input image")


# --------------------------------------------------
# 1. Detect target face
# --------------------------------------------------

target_faces = detector.detect(target_image)

if not target_faces:
    raise Exception("No target face found")


target_face = target_faces[0]

# Get target embedding
target_embedding = recognizer.get_normalized_embedding(
    target_image,
    target_face.landmarks
)


# --------------------------------------------------
# 2. Detect faces in current frame
# --------------------------------------------------

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


# --------------------------------------------------
# 3. Draw remaining faces
# --------------------------------------------------

draw_detections(
    image=image,
    faces=filtered_faces,
    vis_threshold=0.6
)

cv2.imwrite("output.jpg", image)