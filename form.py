import streamlit as st
from commands import *
from streamlit.commands.execution_control import rerun
import datetime


class RoomForm:
    def __init__(self, room_id, room_price, room_status, reg_id, room_guests, room_type, date, admin):
        self.check_out = None
        self.room_id = room_id
        self.room_price = room_price
        self.room_status = room_status
        self.reg_id = reg_id
        self.room_guests = int(room_guests)
        self.room_type = room_type
        self.days = 1
        self.date = date
        self.admin = admin

    def add_to_database(self):
        st.success(f"Room {self.room_id} зарегистрирована успешно!")
    def render_form(self):
        with st.form(f"Form{self.room_id}"):
            if self.room_status == "Свободно":
                tab1, tab2 = st.tabs(["Информация", 'Регистрация'])
                with tab1:
                    col1, col2 = st.columns(2)
                    col1.header(f"Комната {self.room_id}")
                    price = col2.header(f"{self.room_price}")
                    col3, col4 = st.columns(2)
                    col3.text(f"Статус: {self.room_status}")
                    col4.text(f"Число гостей : {self.room_guests}\nТип комнаты: {self.room_type}")
                with tab2:
                    client_name = ""
                    client_passport = ""
                    for i in range(self.room_guests):
                        client_name += "\n" +(st.text_input(f"ФИО {i + 1}"))
                        client_passport += "\n" + (st.text_input(f"Паспорт {i + 1}"))
                    self.days = st.text_input("Кол-во дней", value=1)
                    method = st.radio("Форма Оплаты", options=["Наличные", "Карта", "Перечесление"])
                    if st.form_submit_button("Регистрация"):

                        # print(self.date)
                        self.check_out = self.date + datetime.timedelta(days=int(self.days))
                        check_in(check_in_date=self.date, check_out_date=self.check_out, room_number=self.room_id,
                                 sum=(int(self.days) * int(self.room_price)), admin=self.admin, payment=method,
                                 client_name=client_name, client_passport=client_passport, days=self.days,
                                 category="[Система] Оплата"
                                 )
                        rerun()
            else:
                tab1, tab2 = st.tabs(["Информация", 'Информация о заселении'])
                with tab1:
                    col1, col2 = st.columns(2)
                    col1.header(f"Комната {self.room_id}")
                    price = col2.header(f"{self.room_price}")
                    col3, col4 = st.columns(2)
                    col3.text(f"Статус: {self.room_status}")
                    col4.text(f"Число гостей : {self.room_guests}\nТип комнаты: {self.room_type}")
                with tab2:
                    data = get_checkout_data(self.reg_id)
                    names = data["client_name"].split("\n")
                    client_passport = data["client_passport"].split("\n")
                    for i in range(self.room_guests):
                        st.text_input(f"ФИО {i + 1}", value=f"{names[i+1]}", disabled=True)
                        st.text_input(f"Паспорт {i + 1}", value=f"{client_passport[i+1]}", disabled=True)
                    self.days = st.text_input("Кол-во дней", value=data['days'], disabled=True)
                    payment_options = {
                        "Наличные": 0,
                        "Карта": 1,
                        "Перечесление": 2
                    }
                    method = st.radio("Форма Оплаты", options=["Наличные", "Карта", "Перечесление"], index=payment_options[data["payment_method"]], disabled=True)
                    st.write(f"Дата заселения: {data['check_in_date']}")
                    st.write(f"Дата выселения: {data['check_out_date']}")
                    st.write(f"Сумма к оплате: {data['sum']}")
                    if st.form_submit_button("Выселить"):
                        evict(self.room_id)
                        rerun()
