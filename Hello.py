import streamlit as st
from commands import *
from form import RoomForm

st.set_page_config(
    page_title="Hotel Management System",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",

)

st.title("Welcome to Hotel Management System! 👋")

if __name__ == "__main__":

    logged = False

    username = st.text_input("user")
    password = st.text_input("password")

    try:
        info = sign_in(username)

        if decryption(info[0]["password"]) == password:
            st.success("Success")
            logged = True
        else:
            st.error("Check Username and Password")
    except:
        pass

    if logged:
        rooms = get_rooms()
        print(rooms)
        for room in rooms:
            RoomForm(room_id=room['room_number'], room_price=room['room_price'], room_status=room['room_status'],
                     room_guests=room['room_guests'], room_type=room['room_type']).render_form()
