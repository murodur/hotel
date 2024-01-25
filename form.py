import streamlit as st


class RoomForm:
    def __init__(self, room_id):
        self.room_id = room_id + 1

    def add_to_database(self):
        # Здесь вы можете добавить логику для сохранения данных в базу данных
        st.success(f"Room {self.room_id} зарегистрирована успешно!")
        print(self.room_id)

    def render_form(self):
        with st.form(f"Form{self.room_id}"):
            col1, col2 = st.columns(2)
            col1.header(f"Room {self.room_id}")
            price = col2.header("250000")
            col3, col4 = st.columns(2)
            col3.text("Status: Free")
            col4.text("Some Information")

            if st.form_submit_button("Регистрация"):
                st.text_input("ФИО")
                st.text_input("Паспорт")
                days = st.text_input("Кол-во дней")

                if st.form_submit_button("Добавить", on_click=self.add_to_database):
                    pass


def add_to_database(self):
    print(self)