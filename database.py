import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "maglev.proxy.rlwy.net",
    "port": 50049,
    "user": "root",
    "password": "RMjcOQGoSktiNYXPusuQAALwUomNoEls",
    "database": "railway"
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
