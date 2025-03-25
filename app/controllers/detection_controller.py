from fastapi import APIRouter, UploadFile, File, HTTPException, Request, Depends
import cv2
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from datetime import datetime

# from services.detect_service import detect
from app.db.session import get_db
from app.schemas.student import StudentUpdate
from app.services.student_service import get_student_by_adm, update_student, get_students

router = APIRouter()

@router.post("/detection")
async def detection_endpoint(request:Request, db: Session = Depends(get_db)):
    try:
        adm_no = "771"
        student = get_student_by_adm(db, adm_no)
        try:
            stud_data = StudentUpdate(
                left_at = datetime.now()
            )
            update_student(db, student.id, stud_data)
            return {"student": student}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @router.post("/detection")
# async def detection_endpoint2():
#     try:
#         # Read image file as bytes and convert to OpenCV format
#         # contents = await file.read()
#         # nparr = np.frombuffer(contents, np.uint8)
#         # image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
#         # if image is None:
#         #     raise HTTPException(status_code=400, detail="Invalid image format")

#         # adm_no = detect(image)
#         adm_no = 771
#         student = get_student_by_adm(adm_no)
        
#         # stud_data = StudentUpdate(
#         #     left_at = func.now()
#         # )
#         # update_student(db, student_id, stud_data)
#         return {"student": student}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
