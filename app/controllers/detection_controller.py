from fastapi import APIRouter, Request, Response

router = APIRouter()

@router.post("/detection")
def detect(request: Request):
    return Response("Hello world")