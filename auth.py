import jwt
import datetime

SECRET_KEY = "sua_chave_secreta_super_segura"


def generate_token(user_id: int):
    """Gera um token JWT para autenticação"""
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token
