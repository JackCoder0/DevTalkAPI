import json
from typing import List
from fastapi import APIRouter, HTTPException, Body
from database import get_connection
from schemas.lessons_schema import LessonCompletionRequest, LessonCreate, LessonWithQuestions, QuestionCreate
from utils.functions import *

router = APIRouter()


@router.post("/")
def create_lesson(lesson: LessonCreate):
    conn = get_connection()
    cursor = conn.cursor()

    if not conn:
        raise HTTPException(
            status_code=500, detail="Erro ao conectar ao banco de dados")

    try:
        cursor.callproc("CreateLesson", [
            lesson.title,
            lesson.description,
            lesson.level,
            lesson.section,
            lesson.sprint_number,
            lesson.xp_reward
        ])

        conn.commit()
        return {"message": "Lição criada com sucesso!"}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        cursor.close()
        conn.close()


@router.get("/{lesson_id}", response_model=LessonWithQuestions)
def get_lesson_with_questions(lesson_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc("GetLessonWithQuestions", [lesson_id])

        # Obtemos o primeiro resultado (dados da lição)
        stored_results = list(cursor.stored_results())
        if len(stored_results) < 2:
            raise HTTPException(
                status_code=404, detail="Lesson not found or no questions linked.")

        lesson_result = stored_results[0].fetchone()
        question_result = stored_results[1].fetchall()

        if not lesson_result:
            raise HTTPException(status_code=404, detail="Lesson not found")

        # Decodificar as opções das perguntas
        for question in question_result:
            if isinstance(question.get("options"), str):
                question["options"] = json.loads(question["options"])

        lesson_result["questions"] = question_result
        return lesson_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.post("/questions/")
def create_questions(questions: List[QuestionCreate] = Body(...)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for question in questions:
            cursor.callproc("CreateQuestion", [
                question.lesson_id,
                question.question_text,
                question.type,
                question.correct_answer,
                json.dumps(question.options),
                question.explanation
            ])
        conn.commit()
        return {"message": f"{len(questions)} questões criadas com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.post("/complete")
def complete_lesson(data: LessonCompletionRequest):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Chama a procedure
        cursor.callproc("sp_register_lesson_completion", (
            data.user_id,
            data.lesson_id,
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Lição registrada como concluída com sucesso!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
