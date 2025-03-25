import cv2
import os
from deepface import DeepFace

database_path = "static/DB"

def detect(image):
    # Convert BGR to RGB for DeepFace
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Perform face recognition
    result = DeepFace.find(
        img_path=image,
        db_path=database_path,
        model_name="ArcFace",
        detector_backend="retinaface",
        distance_metric="euclidean_l2"
    )

    if isinstance(result, list) and len(result) > 0:
        df = result[0]  # Extract the first DataFrame

        if not df.empty:
            # Extract the folder (person's name) from the matched image path
            matched_persons = list(set(os.path.basename(os.path.dirname(path)) for path in df["identity"]))

            return {"status": "✅ Match found", "matched_persons": matched_persons}
        else:
            return {"status": "❌ No match found"}
    else:
        return {"status": "❌ No faces found in the database"}