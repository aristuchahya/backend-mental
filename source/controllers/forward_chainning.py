from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from sqlalchemy.orm import Session
from source.databases.db import get_db
from source.services.forward_chainning import ForwardChaining
from source.services.service_admin import ServiceAdmin
from source.schemas.schemas import AssesmentCreate

router = APIRouter(
    prefix="/assesment",
    tags=["assesment"]
)

chain = ForwardChaining()
service = ServiceAdmin()

@router.post("/")
def creating_assesment(payload: AssesmentCreate, db: Session = Depends(get_db)):
    try:
        chain.create_assesment(db, payload)
        
        return {
            "status": "success",
            "message": "Diagnosis 211 successfully created"
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{user_id}")
def get_id(user_id: str, db: Session = Depends(get_db)):
    result = chain.get_asessment_id(db, user_id)

    return {
        "status": "success",
        "asessment_id": result
    }
    
@router.get("/diagnosis/{asesment_id}")
def get_diagnosis_result(asesment_id: str, db: Session = Depends(get_db)):
    try:
        return chain.get_diagnosis(db, asesment_id)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/profile/{user_id}")
def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    try:
        return service.get_user(db, user_id)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        

