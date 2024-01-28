import time

from streamlit.commands.execution_control import rerun
import pandas as pd
import streamlit as st
from commands import *
from form import RoomForm
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(
    page_title="N&J Hotel Management System",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",

)

st.title("Welcome to N&J Hotel Management System! 👋")

def create_form(username):
    rooms = get_rooms()
    # print(rooms)
    for room in rooms:
        RoomForm(room_id=room['room_number'], room_price=room['room_price'],
                 room_status=room['room_status'], reg_id=room["registration_id"],
                 room_guests=room['room_guests'], room_type=room['room_type'], date=new_time,
                 admin=username).render_form()
def create_history():
    with st.form("History"):
        try:
            histories = get_history()
            df = pd.DataFrame(histories)
            df['client_name'] = df['client_name'].str.replace('\n', ' -- ')
            df['client_passport'] = df['client_passport'].str.replace('\n', ' -- ')
            df = df.rename(columns={
                "id": "ID",
                "check_in_date": "Дата Регистрации",
                "check_out_date": "Дата Выезда",
                "days": "Дней",
                "room_number": "Номер Комнаты",
                "sum": "Сумма",
                "admin_username": "Администратор",
                "payment_method": "Метод оплаты",
                "client_name": "Имя Клиента",
                "client_passport": "Паспорт Клиента"
            })
            df = df.iloc[::-1]
            st.table(df)

        except:
            st.header("Ooops. Program occured Error, please contact Telegram: @a_meliev_10")
        if st.form_submit_button("Обновить"):
            rerun()


def create_kassa():
    st.header("Касса")
    t1, t2, t3 = st.tabs(["Общее", "Расход", "Доход"])
    with t1:
        with st.form("Overall"):
            all_money = get_kassa()
            kassa = 0
            for money in all_money:
                kassa += int(money['amount'])
            st.header(f"Касса: {kassa}")
            if st.form_submit_button("Обновить"):
                rerun()
        with st.form("History_for_today"):
            st.header("Последние 24 часа")
            df = pd.DataFrame(get_kassa_table())
            df = df.iloc[::-1]
            st.table(df)
            if st.form_submit_button("Обновить"):
                rerun()
    with t2:
        with st.form("Расходы"):
            amount = st.text_input("Сумма: ")
            category = st.selectbox("Выберите Категорию", ["Зарплата", "Коммунальные услуги", "Продукты",
                                                           "Санитарно-Гигиенические расходы", "Снятие от начальства",
                                                           "Запчасти", "Прочие расходы"])
            comment = st.text_input("Комментарий: ")
            if st.form_submit_button("Добавить"):
                add_to_kassa(username, int(amount) * -1, category, comment)
                rerun()
    with t3:
        with st.form("Доходы"):
            amount = st.text_input("Сумма: ")
            category = st.selectbox("Выберите Категорию", ["Оплата", "Внешние Источники"])
            comment = st.text_input("Комментарий: ")

            if st.form_submit_button("Добавить"):
                add_to_kassa(username, int(amount), category, comment)
                rerun()
def create_analytics():
    tab1, tab2, tab3 = st.tabs(["Финансы", "Работники", "Посещения"])
    with tab1:
        with st.form("Finance"):
            choice = st.number_input("Выберите срок:", min_value=1, max_value=365)

            if st.form_submit_button("Показать"):
                data = get_transactions(choice)
                print()
                positive = data[0]
                negative = data[1]
                external = data[2]

                n_sum = 0
                p_sum = 0
                e_sum = 0
                for i in negative:
                    n_sum += i["amount"]
                for i in positive:
                    p_sum += i['amount']
                for i in external:
                    e_sum += i['amount']
                n_sum = n_sum * -1
                labels = ["Доход", "Расход", "Внешние Источники"]
                sizes = [p_sum, n_sum, e_sum]

                fig = go.Figure(data=[go.Pie(labels=labels, values=sizes)])

                fig.update_layout(
                    title='Общие сведения',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                )

                st.plotly_chart(fig)
                expenses = get_expenses(choice)

                expenses_summary = {
                    "Зарплата": 0,
                    "Коммунальные услуги": 0,
                    "Продукты": 0,
                    "Санитарно-Гигиенические расходы": 0,
                    "Снятие от начальства": 0,
                    "Запчасти": 0,
                    "Прочие расходы": 0,
                    "Неизвестно": 0
                }

                for e in expenses:
                    category = e['category']
                    if category in expenses_summary:
                        expenses_summary[category] += e['amount'] * -1
                    else:
                        expenses_summary["Неизвестно"] += e['amount'] * -1

                labels = list(expenses_summary.keys())
                sizes = list(expenses_summary.values())

                fig = go.Figure(data=[go.Pie(labels=labels, values=sizes)])

                fig.update_layout(
                    title='Распределение расходов по категориям',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                )

                st.plotly_chart(fig)
        with tab2:
            with st.form("Workers"):
                choice_W = st.number_input("Выберите срок:", min_value=1, max_value=365)

                admins = ["Все"]
                adm = get_admins()
                for a in adm:
                    admins.append(a['username'])
                admin_select = st.selectbox("Выберите Админа:", admins)

                type = st.selectbox("Выберите тип графика: ", ["Круглый", "Таблица", "Линейный"])
                if st.form_submit_button("Показать") and 1 <= choice_W <= 365:
                    if type == "Круглый" and admin_select == "Все":
                        adm_data = get_admin_data(admin_select)
                        admin_names = []
                        orders = []
                        for a in adm_data:
                            admin_names.append(a["admin_username"])
                            orders.append(a['total_orders'])

                        # pass
                        labels = admin_names
                        sizes = orders

                        fig = go.Figure(data=[go.Pie(labels=labels, values=sizes)])

                        fig.update_layout(
                            title='Pie Chart',
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                        )

                        st.plotly_chart(fig)
        with tab3:
            with st.form("Посещения"):
                choice_v = st.number_input("Выберите срок:", min_value=1, max_value=365)
                if st.form_submit_button("Показать"):
                    data = get_visitor(choice_v)

                    dates = [entry['visit_date'].strftime('%d-%m-%Y') for entry in data]
                    visit_counts = [entry['visits_count'] for entry in data]

                    fig = go.Figure(data=[go.Bar(x=dates, y=visit_counts)])

                    fig.update_layout(
                        title=f'Количество посетителей за последние {choice_v} дней',
                        xaxis_title='Дата',
                        yaxis_title='Количество посещений'
                    )

                    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":


    logged = False
    time.sleep(4)



    username = st.text_input("user")
    password = st.text_input("password", type='password')

    try:
        info = sign_in(username)

        if decryption(info[0]["password"]) == password:
            st.success("Success")
            logged = True
            check_status()
            timing = get_time()
            new_time = timing["NOW()"] + datetime.timedelta(hours=2)
        else:
            st.error("Check Username and Password")
    except:
        pass

    if logged:
        if get_admin_level(username)[0]['level'] == '3':
            tab1, tab2, tab3, tab4 = st.tabs(["Регистрация", "Касса", "История Регистрации", "Аналитика"])
            with tab1:
                create_form(username)
            with tab2:
                create_kassa()
            with tab3:
               create_history()
            with tab4:
                create_analytics()
        elif get_admin_level(username)[0]['level'] == '2':
            tab1, tab2 = st.tabs(["Регистрация", "Касса"])
            with tab1:
                create_form(username)
            with tab2:
                create_kassa()
        elif get_admin_level(username)[0]['level'] == '1':
            create_form(username)
