from fastapi import APIRouter, UploadFile, File, HTTPException, Request, Depends
import cv2
import numpy as np
from sqlalchemy.orm import Session
from datetime import datetime

from app.services.detect_service import detect
from app.db.session import get_db
from app.schemas.student import StudentUpdate
from app.services.message_service import send_whatsapp_message
from app.services.student_service import get_student_by_adm, update_student, get_students

router = APIRouter()

@router.post("/detection")
async def detection_endpoint(request:Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        detection_result = detect(image)

        if detection_result["status"] == "success":
            adm_no = detection_result["admission"]

            student = get_student_by_adm(db, adm_no)
            try:
                stud_data = StudentUpdate(
                    left_at = datetime.now()
                )
                update_student(db, student.id, stud_data)

                # formatted_time = student.left_at.strftime("%A of %-dth %B %Y at %-I:%M %p")

                # Handle the suffix for the day (st, nd, rd, th)
                def day_suffix(day):
                    if 11 <= day <= 13:
                        return "th"
                    return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

                day = student.left_at.day
                suffix = day_suffix(day)
                formatted_day = student.left_at.strftime(f"%A of {day}{suffix} %B %Y at %-I:%M %p")

                # Final message
                # message =
                data = {
                    "phone": student.parent.phone,
                    "message": f"{student.parent.first_name} {student.parent.last_name}, your child {student.full_name} has left the school on the {formatted_day}"
                }
                send_whatsapp_message(data)
                return {"message": data["message"]}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

