from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from sqlalchemy.orm import Session
from source.databases.db import get_db
from source.services.service_admin import ServiceAdmin
from source.schemas.schemas import UserRequest, UserResponse, RuleRequest, MentalDisorderRequest

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

service = ServiceAdmin()

@router.post("/upload-excel")
def import_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        service.upload_data(db, file)

        return {
            "status": "success",
            "message": "Data successfully import to database"
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/create-user")
def create_user(payload: UserRequest, db: Session = Depends(get_db)):
    try:
        return service.create_user(db, payload)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@router.get("/all-assesment")
def get_all_assesment(db: Session = Depends(get_db)):
    try:
        return service.get_assesments(db)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/assesment/{user_id}")
def assesment_by_user(user_id: str, db: Session = Depends(get_db)):
    try:
        return service.get_assesment_by_user(db, user_id)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/questions")
def get_all_questions(db: Session = Depends(get_db)):
    try:
        questions = service.get_questions(db)
        if not questions:
            return HTTPException(status_code=404, detail="Questions not found")

        return questions

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/rules")
def get_all_rule(db: Session = Depends(get_db)):
    try:
        rules = service.get_rules(db)
        if not rules:
            return HTTPException(status_code=404, detail="Rules not found")

        return rules

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/create-rule")
def add_rule(payload: RuleRequest, db: Session = Depends(get_db)):
    try:
        return service.create_rule(db, payload)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/rule/{rule_id}")
def get_rules_by_id(rule_id: str, db: Session = Depends(get_db)):
    try:
        return service.get_rule_by_id(db, rule_id)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.patch("/rule/{rule_id}")
def update_rules(rule_id: str, payload: RuleRequest, db: Session = Depends(get_db)):
    try:
        return service.update_rule(db, rule_id, payload)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/rule/{rule_id}")
def delete_rules(rule_id: str, db: Session = Depends(get_db)):
    try:
        return service.delete_rule(db, rule_id)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/mental-disorder")
def get_all_mental_disorder(db: Session = Depends(get_db)):
    try:
        return service.get_mental_disorders(db)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/mental-disorder/{mental_id}")
def get_mental_disorder_by_id(mental_id: str, db: Session = Depends(get_db)):
    try:
        return service.get_mental_by_id(db, mental_id)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.patch("/mental-disorder/{mental_id}")
def update_mental_disorders(mental_id: str, payload: MentalDisorderRequest, db: Session = Depends(get_db)):
    try:
        return service.update_mental_disorder(db, mental_id, payload)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/mental-disorder")
def add_mental_disorder(payload: MentalDisorderRequest, db: Session = Depends(get_db)):
    try:
        return service.create_mental_disorder(db, payload)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/all-diagnosis")
def all_diagnosis(db: Session = Depends(get_db)):
    try:
        return service.get_all_diagnosis(db)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))