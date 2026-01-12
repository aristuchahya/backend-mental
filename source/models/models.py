from source.databases.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from cuid2 import cuid_wrapper, Cuid
from datetime import datetime

cuid : Cuid = Cuid(length=10)

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: cuid.generate())
    nama = Column(String, nullable=True)
    jenis_kelamin = Column(String, nullable=True)
    umur = Column(Integer, nullable=True)
    noip = Column(String, nullable=True)
    tanggal = Column(DateTime, nullable=True)
    whatsapp = Column(String, nullable=True) 
    nama_orangtua = Column(String, nullable=True)
    prodi = Column(String, nullable=True)
    semester = Column(String, nullable=True)
    asuransi = Column(String, nullable=True)

class Admin(Base):
    __tablename__ = "admin"

    id = Column(String, primary_key=True, default=lambda: cuid.generate())
    nama = Column(String, nullable=True)
    username = Column(String, nullable=True, unique=True)
    role = Column(String, nullable=True)
    password = Column(String, nullable=True)


class Question(Base):
    __tablename__ = "questions"

    id = Column(String, primary_key=True, default=lambda: cuid.generate())
    code = Column(String, nullable=True, unique=True)
    text = Column(Text, nullable=True)
    category = Column(String, nullable=True)



class Assesment(Base):
    __tablename__ = "assesments"

    id = Column(String, primary_key=True, default=lambda: cuid.generate())
    user_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now())

class Answer(Base):
    __tablename__ = "answers"

    id = Column(String, primary_key=True, default=lambda: cuid.generate())
    question_code = Column(String, ForeignKey('questions.code'))
    assesment_id = Column(String, ForeignKey('assesments.id'))
    value = Column(Integer, nullable=False)

class Rule(Base):
    __tablename__ = "rules"

    id = Column(String, primary_key=True, default=lambda: cuid.generate())
    category = Column(String)
    min_score = Column(Integer)
    max_score = Column(Integer)
    level = Column(String)

class Score(Base):
    __tablename__ = "scores"

    id = Column(String, primary_key=True, default=lambda: cuid.generate())
    assesment_id = Column(String, ForeignKey("assesments.id"))
    category = Column(String)
    raw_score = Column(Integer)
    final_score = Column(Integer)

class DiagnosisResult(Base):
    __tablename__ = "diagnosis_results"

    id = Column(String, primary_key=True, default=lambda: cuid.generate())
    assesment_id = Column(String, ForeignKey("assesments.id"))
    category = Column(String)
    level = Column(String)
    created_at = Column(DateTime, default=datetime.now())

    mental_disorder_id = Column(
        String,
        ForeignKey("mental_disorders.id"),
        nullable=True
    )

class MentalDisorder(Base):
    __tablename__ = "mental_disorders"

    id = Column(String, primary_key=True, default=lambda: cuid.generate())
    category = Column(String) 
    level = Column(String)     
    name = Column(String)
    description = Column(Text)
    solution = Column(Text)
