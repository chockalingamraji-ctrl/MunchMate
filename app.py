import streamlit as st

st.set_page_config(
    page_title="MunchMate",
    page_icon="🍽️",
    layout="wide"
)

st.title("🍽️ MunchMate")

st.subheader("Fresh, affordable vegetarian breakfast for students")

st.write("Choose your role")

col1, col2 = st.columns(2)

with col1:
    if st.button("🎓 Student"):
        st.success("Student Portal Selected")

with col2:
    if st.button("🔒 Admin"):
        st.success("Admin Portal Selected")
