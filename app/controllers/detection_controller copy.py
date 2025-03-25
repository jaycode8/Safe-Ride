from fastapi import APIRouter, Request, Response
import cv2
import matplotlib.pyplot as plt
from deepface import DeepFace

router = APIRouter()
database_path = ""

@router.post("/detection")
def detect(request: Request):
    image = cv2.imread(test_image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
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
            matched_persons = set(os.path.basename(os.path.dirname(path)) for path in df["identity"])

            print(f"✅ Match found: {', '.join(matched_persons)}")
        else:
            print("❌ No match found.")
    else:
        print("❌ No faces found in the database.")
    return Response("Hello world")