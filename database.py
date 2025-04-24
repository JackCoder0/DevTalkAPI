import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "",
    "port": 0,
    "user": "",
    "password": "",
    "database": ""
}


def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None


# if __name__ == "__main__":
#     conn = get_connection()
#     if conn:
#         print("✅ Conexão bem-sucedida!")
#         conn.close()
#     else:
#         print("❌ Falha na conexão!")
