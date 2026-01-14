from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AnswerInput(BaseModel):
    question_code: str
    value: int

class AssesmentCreate(BaseModel):
    user_id: str
    answers: List[AnswerInput]

class UserRequest(BaseModel):
    nama : str
    jenis_kelamin : str
    umur : int
    noip : Optional[str] = None
    tanggal : datetime
    whatsapp : str
    nama_orangtua : Optional[str]
    prodi : Optional[str]
    semester : Optional[str]
    asuransi : Optional[str] = None

class UserResponse(UserRequest):
    id : str
    model_config = {
        "from_attributes": True
    }

class RuleRequest(BaseModel):
    category : str
    min_score : int
    max_score : int
    level : str

class RuleResponse(RuleRequest):
    id : str
    model_config = {
        "from_attributes": True
    }

class MentalDisorderRequest(BaseModel):
    name : str
    category: str
    level: str
    description: str
    solution: str
    
