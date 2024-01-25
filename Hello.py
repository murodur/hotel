import streamlit as st

from form import RoomForm


st.set_page_config(
    page_title="Hotel Management System",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",

)

st.title("Welcome to Hotel Management System! 👋")

if __name__ == "__main__":
    rooms = 11
    user = "root"
    passwd = "root"
    logged = False

    # with st.form("auth", clear_on_submit=True):
    #     username = st.text_input("user")
    #     password = st.text_input("password")
    #     if st.form_submit_button("Log in"):
    #         if username == user and password == passwd:
    #             st.success("Success")
    #             logged = True
    #         else:
    #             st.error("Check Username and Password")

    username = st.text_input("user")
    password = st.text_input("password")
    if username == user and password == passwd:
        st.success("Success")
        logged = True
    else:
        st.error("Check Username and Password")

    if logged:
        for i in range(rooms):
            RoomForm(i).render_form()
