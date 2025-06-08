import numpy as np
from deepface import DeepFace


def get_faces(pixels: np.array) -> list[dict]:
    """
    Detect faces in an image using DeepFace and return their bounding boxes and confidence scores.
    :param pixels: Image data as a numpy array.
    :return: List of dictionaries containing bounding box coordinates and confidence scores for each detected face.
    """
    
    result = DeepFace.analyze(
        img_path=pixels, actions=['age']
    )

    return [
        {
            "box": [
                int(face["region"]["x"]),
                int(face["region"]["y"]),
                int(face["region"]["w"]),
                int(face["region"]["h"]),
            ],
            "confidence": face["face_confidence"]
        }
        for face in result
    ]
