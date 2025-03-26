import cv2
import os
from deepface import DeepFace

database_path = "static/DB"

def detect(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    result = DeepFace.find(
        img_path=image,
        db_path=database_path,
        model_name="ArcFace",
        detector_backend="retinaface",
        distance_metric="euclidean_l2"
    )

    if isinstance(result, list) and len(result) > 0:
        df = result[0]

        if not df.empty:
            admission = list(set(os.path.basename(os.path.dirname(path)) for path in df["identity"]))
            print(admission)
            return {"status": "success", "admission": admission}
        else:
            return {"status": "fail"}
    else:
        return {"status": "fail"}