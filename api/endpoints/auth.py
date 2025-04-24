from binascii import Error
from fastapi import APIRouter, HTTPException

from auth import generate_token
from database import get_connection
from schemas.auth_schema import LoginRequest, UserCreate
from utils.functions import *

router = APIRouter()


@router.post("/register/")
def register_user(user: UserCreate):
    conn = get_connection()
    if not conn:
        raise HTTPException(
            status_code=500, detail="Erro ao conectar ao banco de dados")

    try:
        cursor = conn.cursor()
        cursor.callproc("CreateUser", [
            user.name, user.email, user.password_hash, user.auth_provider, user.age, 0
        ])

        cursor.execute("SELECT LAST_INSERT_ID();")
        user_id = cursor.fetchone()[0]

        conn.commit()
        return {"message": "Usuário registrado com sucesso!", "user_id": user_id}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        cursor.close()
        conn.close()


@router.post("/login/")
def login(login: LoginRequest):
    conn = get_connection()
    if not conn:
        raise HTTPException(
            status_code=500, detail="Erro ao conectar ao banco de dados"
        )

    try:
        cursor = conn.cursor(dictionary=True)

        cursor.callproc("LoginUser", [login.user, login.password])

        user_data = None
        for result in cursor.stored_results():
            user_data = result.fetchall()

        if not user_data:
            raise HTTPException(
                status_code=401, detail="E-mail ou senha incorretos!"
            )

        user_info = user_data[0]

        token = generate_token(user_info["id"])

        return {"user": user_info, "token": token}

    except Error as e:
        conn.rollback()
        raise HTTPException(
            status_code=400, detail=f"Erro no banco de dados: {e}")

    finally:
        cursor.close()
        conn.close()
