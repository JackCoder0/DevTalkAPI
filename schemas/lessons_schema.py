from typing import Dict, List, Optional
from pydantic import BaseModel


class LessonCreate(BaseModel):
    title: str
    description: Optional[str]
    level: str
    section: int
    sprint_number: int
    xp_reward: Optional[int] = 50

    class Config:
        orm_mode = True


class QuestionCreate(BaseModel):
    lesson_id: int
    question_text: str
    type: str
    correct_answer: str
    options: List[str] = None
    explanation: Optional[str] = None

    class Config:
        orm_mode = True


class Question(BaseModel):
    question_id: int
    lesson_id: int
    question_text: str
    type: str
    correct_answer: str
    options: List[str]
    explanation: Optional[str]

    class Config:
        orm_mode = True


class LessonWithQuestions(BaseModel):
    lesson_id: int
    title: str
    description: str
    level: str
    xp_reward: int
    questions: List[Question]

    class Config:
        orm_mode = True


class LessonCompletionRequest(BaseModel):
    user_id: int
    lesson_id: int

    class Config:
        orm_mode = True
