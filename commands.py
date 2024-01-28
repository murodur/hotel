import pymysql
from config import host, port, user, password, db_name
from encryption import encryption, decryption
import datetime

connection = pymysql.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=db_name,
    cursorclass=pymysql.cursors.DictCursor
)


def sign_in(name: str) -> bool:
    with connection.cursor() as cursor:
        command = f"""
                    Select * FROM admins WHERE username = '{name}'
        """
        cursor.execute(command)
        profile = cursor.fetchall()
        cursor.close()
        return False if len(profile) == 0 else profile

def get_time():

    with connection.cursor() as cursor:
        command = """SELECT NOW()"""
        cursor.execute(command)
        time_db = cursor.fetchall()
        cursor.close()

        return time_db[0]


def evict(room_number):

    with connection.cursor() as cursor:
        command = f"""UPDATE `rooms` SET `room_status`='Свободно', `registration_id`='0' WHERE `room_number`='{room_number}'"""
        cursor.execute(command)
        connection.commit()
        cursor.close()



def check_in(check_in_date, check_out_date, days, room_number, sum, admin, payment, client_name, client_passport, category):

    with connection.cursor() as cursor:
        insert_command = """INSERT INTO `registration_book`
             (`check_in_date`, `check_out_date`, `days`, `room_number`, `sum`, `admin_username`, `payment_method`, 
             `client_name`, `client_passport`) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(insert_command,
                       (check_in_date, check_out_date, days, room_number, sum, admin, payment, client_name, client_passport))

        registration_id = cursor.lastrowid

        update_command = "UPDATE `rooms` SET `room_status`='Заселен', `registration_id`=%s WHERE `room_number`=%s"
        cursor.execute(update_command, (registration_id, room_number))
        kassa_command = F"""INSERT INTO `kassa`(`admin`, `amount`, `category`, `timing`, `comment`) 
        VALUES 
        ('{admin}','{int(sum)}', '{category}','{check_in_date}', '[СИСТЕМА] ОПЛАТА ЗА КОМНАТУ {room_number}, ЧЕК {registration_id}')"""
        cursor.execute(kassa_command)
        connection.commit()
        cursor.close()



def get_kassa():

    with connection.cursor() as cursor:
        command = f"SELECT `amount` FROM `kassa`"
        cursor.execute(command)

        data = cursor.fetchall()

        cursor.close()

        return data


def add_to_kassa(username, amount, category, comment):

    with connection.cursor() as cursor:
        timing = get_time()["NOW()"] + datetime.timedelta(hours=2)
        command = f"""INSERT INTO `kassa`(`admin`, `amount`, `category`, `timing`, `comment`) 
                      VALUES 
                      ('{username}','{int(amount)}', '{category}', '{timing}','{comment}')"""
        cursor.execute(command)
        connection.commit()
        cursor.close()

def get_kassa_table():

    with connection.cursor() as cursor:
        command = f"""SELECT *
                      FROM kassa
                      WHERE timing >= DATE_SUB(NOW(), INTERVAL 1 DAY)"""
        cursor.execute(command)
        data = cursor.fetchall()

        cursor.close()

        return data
def get_admin_level(username):

    with connection.cursor() as cursor:
        command = f"SELECT `level` FROM `admins` WHERE `username`='{username}'"
        cursor.execute(command)

        level = cursor.fetchall()

        cursor.close()

        return level


def get_checkout_data(reg_id):

    with connection.cursor() as cursor:
        command = "SELECT * FROM `registration_book` WHERE `id`=%s"
        cursor.execute(command, (reg_id,))
        data = cursor.fetchone()
        cursor.close()

        return data


def get_history():

    with connection.cursor() as cursor:
        command = "SELECT * FROM `registration_book`"
        cursor.execute(command)
        data = cursor.fetchall()
        cursor.close()

        return data
def get_rooms():

    with connection.cursor() as cursor:
        command = f"""
            SELECT * FROM rooms;
        """
        cursor.execute(command)
        rooms = cursor.fetchall()
        cursor.close()

        return rooms

def check_status():

    with connection.cursor() as cursor:
        command = "SELECT registration_id FROM rooms"
        cursor.execute(command)
        data = cursor.fetchall()
        for d in data:
            if d['registration_id'] != 0:
                timing = get_time()
                reg_data_command = f"SELECT check_out_date FROM registration_book WHERE id = {d['registration_id']};"
                cursor.execute(reg_data_command)
                reg_data = cursor.fetchone()
                if reg_data['check_out_date'] <= timing['NOW()']:
                    update_command = f"""UPDATE `rooms` SET `room_status`='Свободно', `registration_id`='0' WHERE `registration_id`='{d['registration_id']}'"""
                    cursor.execute(update_command)
                connection.commit()
                cursor.close()



def get_transactions(days):
    with connection.cursor() as cursor:
        income_command = f"""SELECT `amount`
                             FROM kassa
                             WHERE amount > 0 AND category != 'внешние источники' AND timing >= DATE_SUB(NOW(), INTERVAL {int(days)} DAY);"""
        cursor.execute(income_command)
        incomes = cursor.fetchall()

        expense_command = f"""SELECT `amount`
                              FROM kassa
                              WHERE amount < 0 AND timing >= DATE_SUB(NOW(), INTERVAL {int(days)} DAY);"""
        cursor.execute(expense_command)
        expenses = cursor.fetchall()

        external_command = f"""SELECT `amount`
                               FROM kassa
                               WHERE category = 'внешние источники' AND timing >= DATE_SUB(NOW(), INTERVAL {int(days)} DAY);"""
        cursor.execute(external_command)
        externals = cursor.fetchall()

        cursor.close()

        return incomes, expenses, externals
def get_admins():
    with connection.cursor() as cursor:
        command = f"""SELECT `username`
                      FROM admins"""
        cursor.execute(command)
        data = cursor.fetchall()
        cursor.close()

        return data


def get_admin_data(username):

    with connection.cursor() as cursor:
        if username != "Все":
            command = f"""SELECT * FROM registration_book WHERE `admin_username`={username}"""
        else:
            command = f"""SELECT admin_username, COUNT(*) as total_orders
                          FROM registration_book
                          GROUP BY admin_username;"""
        cursor.execute(command)
        data = cursor.fetchall()
        cursor.close()

        return data


def get_expenses(days):

    with connection.cursor() as cursor:
        command = f"""SELECT `category`, `amount`
                      FROM kassa
                      WHERE amount < 0 AND timing >= DATE_SUB(NOW(), INTERVAL {int(days)} DAY);"""
        cursor.execute(command)
        expenses = cursor.fetchall()


        cursor.close()

        return expenses


def get_visitor(days):

    with connection.cursor() as cursor:
        command = f"""SELECT DATE(check_in_date) AS visit_date, COUNT(*) AS visits_count
                      FROM registration_book
                      WHERE check_in_date >= DATE_SUB(CURDATE(), INTERVAL {days} DAY)
                      GROUP BY DATE(check_in_date)
                      ORDER BY visit_date DESC;
"""
        cursor.execute(command)

        visit_count_by_day = cursor.fetchall()

        cursor.close()

        return visit_count_by_day
