import streamlit as st

st.set_page_config(
    page_title="MunchMate",
    page_icon="🍽️",
    layout="wide"
)

# Session State
if "page" not in st.session_state:
    st.session_state.page = "home"

# HOME PAGE
if st.session_state.page == "home":

    st.title("🍽️ MunchMate")
    st.subheader("Fresh, affordable vegetarian breakfast for students")

    st.write("Choose your role")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎓 Student"):
            st.session_state.page = "student"
            st.rerun()

    with col2:
        if st.button("🔒 Admin"):
            st.session_state.page = "admin"
            st.rerun()

# STUDENT PAGE
elif st.session_state.page == "student":

    st.title("🎓 Student Portal")

   name = st.text_input("Student Name")

class_name = st.selectbox(
    "Class",
    ["3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
)

section = st.selectbox(
    "Section",
    ["A", "B", "C", "D"]
)

roll_no = st.text_input("Roll Number")

    if st.button("Continue"):

        st.success(f"Welcome {name}")

        st.subheader("Breakfast Menu")

        st.write("🌯 Classic Veg Burrito - ₹45")
        st.write("🌯 Paneer Burrito - ₹55")
        st.write("🥪 Classic Veg Sandwich - ₹25")
        st.write("🥪 Cheese Sandwich - ₹35")
        st.write("🍰 Chocolate Cake Pop - ₹20")
        st.write("🍰 Vanilla Cake Pop - ₹20")
        st.write("🥤 Orange Juice - ₹25")
        st.write("🥤 Watermelon Juice - ₹25")

# ADMIN PAGE
elif st.session_state.page == "admin":

    st.title("🔒 Admin Login")

    password = st.text_input(
        "Enter Passcode",
        type="password"
    )

    secret = st.text_input(
        "Enter Secret Code",
        type="password"
    )

    if st.button("Login"):

        if password == "MunchMate2027" and secret == "MMADMIN":
            st.success("Access Granted")

        else:
            st.error("Invalid Credentials")
