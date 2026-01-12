from sqlalchemy.orm import Session
from fastapi import HTTPException
from source.models.models import (
    Question,
    Answer,
    Assesment,
    DiagnosisResult,
    Rule,
    Score,
    MentalDisorder,
    User
)
from source.schemas.schemas import AssesmentCreate

class ForwardChaining:
    def __init__(self):
        pass
    def forward_chain(self, db: Session, assesment_id: str):
        try:
            answers = (
                db.query(Answer, Question)
                .join(Question, Answer.question_code == Question.code)
                .filter(Answer.assesment_id == assesment_id)
                .all()
            )

            facts = {
                "Depresi": [],
                "Kecemasan": [],
                "Stres": [],
            }

            for answer, question in answers:
                facts[question.category].append(answer.value)
            
            for category, values in facts.items():
                raw_score = sum(values)
                final_score = raw_score * 2

                db.add(Score(
                    assesment_id=assesment_id,
                    category=category,
                    raw_score=raw_score,
                    final_score=final_score
                ))

                rule = db.query(Rule).filter(
                    Rule.category == category,
                    Rule.min_score <= final_score,
                    Rule.max_score >= final_score
                ).first()

                if rule:
                    disorder = db.query(MentalDisorder).filter(
                        MentalDisorder.category == category,
                        MentalDisorder.level == rule.level
                    ).first()

                    db.add(DiagnosisResult(
                        assesment_id=assesment_id,
                        category=category,
                        level=rule.level,
                        mental_disorder_id=disorder.id if disorder else None
                    ))
            
            db.commit()


        except Exception as e:
            db.rollback()
            raise e
        

    def create_assesment(self, db: Session, payload: AssesmentCreate):
        try:
            assesment = Assesment(user_id=payload.user_id)

            db.add(assesment)
            db.commit()
            db.refresh(assesment)

            for a in payload.answers:
                db.add(Answer(
                    assesment_id=assesment.id,
                    question_code=a.question_code,
                    value=a.value
                ))

            db.commit()

            self.forward_chain(db, assesment.id)

            

        except Exception as e:
            db.rollback()
            raise e
        
    
    def get_asessment_id(self, db: Session, user_id: str):
        assessment = (
            db.query(Assesment)
            .filter(Assesment.user_id == user_id)
            .first()
        )

        if not assessment:
            raise HTTPException(
                status_code=404,
                detail="Assessment not found"
            )

        return assessment.id

    def get_diagnosis(self, db: Session, assesment_id: str):
        try:
            results = (
                db.query(DiagnosisResult, MentalDisorder)
                .join(MentalDisorder, DiagnosisResult.mental_disorder_id == MentalDisorder.id)
                .filter(DiagnosisResult.assesment_id == assesment_id)
                .all()
            )
            scores = (
                db.query(Score)
                .filter(Score.assesment_id == assesment_id)
                .all()
            )

            return {
                "assessment_id": assesment_id,
                "scores": [
                    {
                        "category": s.category,
                        "raw_score": s.raw_score,
                        "final_score": s.final_score
                    } for s in scores
                ],
                "results": [
                    {
                        "category": r.category,
                        "level": r.level,
                        "disease": m.name if m else None,
                        "description": m.description if m else None,
                        "solution": m.solution if m else None
                    } for r, m in results
                ]
            }

        except Exception as e:
            db.rollback()
            raise e
    