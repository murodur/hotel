import streamlit as st


class RoomForm:
    def __init__(self, room_id, room_price, room_status, room_guests, room_type):
        self.room_id = room_id
        self.room_price = room_price
        self.room_status = room_status
        self.room_guests = int(room_guests)
        self.room_type = room_type

    def add_to_database(self):
        st.success(f"Room {self.room_id} зарегистрирована успешно!")
        print(self.room_id)

    def render_form(self):
        with st.form(f"Form{self.room_id}"):
            col1, col2 = st.columns(2)
            col1.header(f"Комната {self.room_id}")
            price = col2.header(f"{self.room_price}")
            col3, col4 = st.columns(2)
            col3.text(f"Статус: {self.room_status}")
            col4.text(f"Число гостей : {self.room_guests}\nТип комнаты: {self.room_type}")

            if st.form_submit_button("Регистрация"):
                for i in range(self.room_guests):
                    st.text_input(f"ФИО {i + 1}")
                    st.text_input(f"Паспорт {i + 1}")
                st.text_input("Кол-во дней", key="days", value=1)
                method = st.radio("Форма Оплаты", options=["Наличные", "Карта", "Перечесление"])
                total_price = st.text(f"Сумма к оплате: {int(st.session_state.days) * int(self.room_price)}")

                if st.form_submit_button("Добавить", on_click=self.add_to_database):
                    pass


def add_to_database(self):
    print(self)