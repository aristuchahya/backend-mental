from fastapi import File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
import pandas as pd
from source.models.models import Question, Rule, MentalDisorder, User, Assesment, DiagnosisResult
from source.schemas.schemas import UserRequest, RuleRequest, MentalDisorderRequest

class ServiceAdmin:
    def __init__(self):
        pass

    def create_user(self, db: Session, payload:UserRequest):
        try:
            user = User(
                nama=payload.nama,
                jenis_kelamin=payload.jenis_kelamin,
                umur=payload.umur,
                noip=payload.noip,
                tanggal=payload.tanggal,
                whatsapp=payload.whatsapp,
                nama_orangtua=payload.nama_orangtua,
                prodi=payload.prodi,
                semester=payload.semester,
                asuransi=payload.asuransi
            )
            db.add(user)
            db.commit()
            db.refresh(user)

            return {
                "status": "success",
                "message": "User successfully created",
                "data": user
            }

        except Exception as e:
            db.rollback()
            raise e
    
    def get_user(self, db: Session, user_id: str):
        try:
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                return HTTPException(status_code=404, detail="User not found")

            return {
                "status": "success",
                "data": user
            }

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def upload_data(self, db: Session, file: UploadFile):
        try:
            xls = pd.ExcelFile(file.file)
        except Exception as e:
            raise HTTPException(status_code=400, detail="File harus berformat excel")
        

        if "questions" in xls.sheet_names:
            df_q = pd.read_excel(xls, sheet_name="questions")

            for _, row in df_q.iterrows():
                exists = db.query(Question).filter(Question.code == row["code"]).first()

                if not exists:
                    db.add(Question(
                        code=row["code"],
                        text=row["text"],
                        category=row["category"]
                    ))
        
        if "rules" in xls.sheet_names:
            df_r = pd.read_excel(xls, sheet_name="rules")

            for _, row in df_r.iterrows():
                db.add(Rule(
                    category=row["category"],
                    min_score=int(row["min_score"]),
                    max_score=int(row["max_score"]),
                    level=row["level"]
                ))
        
        if "mental_disorders" in xls.sheet_names:
            df_md = pd.read_excel(xls, sheet_name="mental_disorders")

            for _, row in df_md.iterrows():
                db.add(MentalDisorder(
                    category=row["category"],
                    level=row["level"],
                    name=row["name"],
                    description=row["description"],
                    solution=row["solution"]
                ))

        db.commit()
    
    def get_assesments(self, db: Session):

            return db.query(Assesment).all()


    
    def get_assesment_by_user(self, db: Session, user_id: str):

            assesment = db.query(Assesment).filter(Assesment.user_id == user_id).first()

            if not assesment:
                return HTTPException(status_code=404, detail="Assesment not found")

            return assesment


    
    def get_questions(self, db: Session):

            return db.query(Question).all()


    def get_rules(self, db: Session):

            return db.query(Rule).all()


    
    def create_rule(self, db: Session, payload: RuleRequest):

            rule = Rule(
                category=payload.category,
                min_score=payload.min_score,
                max_score=payload.max_score,
                level=payload.level
            )

            db.add(rule)
            db.commit()
            db.refresh(rule)

            return {
                "status": "success",
                "message": "Rule successfully created",
                "data": rule
            }


    
    def get_rule_by_id(self, db: Session, rule_id: str):

            rule = db.query(Rule).filter(Rule.id == rule_id).first()

            if not rule:
                return HTTPException(status_code=404, detail="Rule not found")

            return rule


    
    def update_rule(self, db: Session, rule_id: str, payload: RuleRequest):
        
            rule = db.query(Rule).filter(Rule.id == rule_id).first()

            if not rule:
                return HTTPException(status_code=404, detail="Rule not found")

            rule.category = payload.category
            rule.min_score = payload.min_score
            rule.max_score = payload.max_score
            rule.level = payload.level

            db.commit()
            db.refresh(rule)

            return {
                "status": "success",
                "message": "Rule successfully updated",
                "data": rule
            }

    def delete_rule(self, db: Session, rule_id: str):
            rule = db.query(Rule).filter(Rule.id == rule_id).first()

            if not rule:
                return HTTPException(status_code=404, detail="Rule not found")

            db.delete(rule)
            db.commit()

            return {
                "status": "success",
                "message": "Rule successfully deleted"
            }


    
    def get_mental_disorders(self, db: Session):
        
            return db.query(MentalDisorder).all()

        
    
    def get_mental_by_id(self, db: Session, mental_id: str):
        
            mental = db.query(MentalDisorder).filter(MentalDisorder.id == mental_id).first()

            if not mental:
                return HTTPException(status_code=404, detail="Mental Disorder not found")

            return mental


    
    def create_mental_disorder(self, db: Session, payload: MentalDisorderRequest):
        try:
            mental = MentalDisorder(
                category=payload.category,
                level=payload.level,
                name=payload.name,
                description=payload.description,
                solution=payload.solution
            )

            db.add(mental)
            db.commit()
            db.refresh(mental)

            return {
                "status": "success",
                "message": "Mental Disorder successfully created",
                "data": mental
            }

        except Exception as e:
            db.rollback()
            raise e
    
    def update_mental_disorder(self, db: Session, mental_id: str, payload: MentalDisorderRequest):
        try:
            mental = db.query(MentalDisorder).filter(MentalDisorder.id == mental_id).first()

            if not mental:
                return HTTPException(status_code=404, detail="Mental Disorder not found")

            mental.category = payload.category
            mental.level = payload.level
            mental.name = payload.name
            mental.description = payload.description
            mental.solution = payload.solution

            db.commit()
            db.refresh(mental)

            return {
                "status": "success",
                "message": "Mental Disorder successfully updated",
                "data": mental
            }

        except Exception as e:
            db.rollback()
            raise e
    
    def get_asessments(self, db: Session):
        return db.query(Assesment).all()
    
    def get_all_diagnosis(self, db: Session):
        results = (
            db.query(DiagnosisResult, User, MentalDisorder, Assesment)
            .join(Assesment, DiagnosisResult.assesment_id == Assesment.id)
            .join(User, Assesment.user_id == User.id)
            .join(MentalDisorder, DiagnosisResult.mental_disorder_id == MentalDisorder.id)
            .all()
        )

        return {
            "status": "success",
            "results": [
                {
                    "nama": user.nama,
                    "category": mental.category,
                    "level": mental.level,
                    "disease": mental.name,
                    "assessment_id": assesment.id
                }
                for diagnosis, user, mental, assesment in results
            ]
        }


