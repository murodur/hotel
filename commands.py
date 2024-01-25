import pymysql
from config import host, port, user, password, db_name
from encryption import encryption, decryption
try:
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("[INFO] Connected to MYSQL DataBase")


except Exception as ex:
    print(ex)
def sign_in(name: str) -> bool:
    with connection.cursor() as cursor:
        command = f"""
                    Select * FROM admins WHERE username = '{name}'
        """
        cursor.execute(command)
        profile = cursor.fetchall()
        return False if len(profile) == 0 else profile

def get_rooms():
    with connection.cursor() as cursor:
        command = f"""
            SELECT * FROM rooms;
        """
        cursor.execute(command)
        rooms = cursor.fetchall()
        return rooms

