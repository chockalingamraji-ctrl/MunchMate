import streamlit as st

st.set_page_config(
    page_title="MunchMate",
    page_icon="🍽️",
    layout="wide"
)

# Session State
if "page" not in st.session_state:
    st.session_state.page = "home"

if "student_details_done" not in st.session_state:
    st.session_state.student_details_done = False


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
        ["6", "7", "8", "9", "10", "11", "12"]
    )

    section = st.selectbox(
        "Section",
        ["A", "B", "C", "D"]
    )

    roll_no = st.text_input("Roll Number")

    if st.button("Continue"):
        st.session_state.student_details_done = True

    if st.session_state.student_details_done:

        st.success(f"Welcome {name}")

        st.subheader("🍽️ Breakfast Menu")

        burrito_classic = st.number_input(
            "🌯 Classic Veg Burrito (₹45)",
            min_value=0,
            value=0
        )

        burrito_paneer = st.number_input(
            "🌯 Paneer Burrito (₹55)",
            min_value=0,
            value=0
        )

        sandwich_classic = st.number_input(
            "🥪 Classic Veg Sandwich (₹25)",
            min_value=0,
            value=0
        )

        sandwich_cheese = st.number_input(
            "🥪 Cheese Sandwich (₹35)",
            min_value=0,
            value=0
        )

        cake_choco = st.number_input(
            "🍰 Chocolate Cake Pop (₹20)",
            min_value=0,
            value=0
        )

        cake_vanilla = st.number_input(
            "🍰 Vanilla Cake Pop (₹20)",
            min_value=0,
            value=0
        )

        juice_orange = st.number_input(
            "🥤 Orange Juice (₹25)",
            min_value=0,
            value=0
        )

        juice_watermelon = st.number_input(
            "🥤 Watermelon Juice (₹25)",
            min_value=0,
            value=0
        )

        total = (
            burrito_classic * 45 +
            burrito_paneer * 55 +
            sandwich_classic * 25 +
            sandwich_cheese * 35 +
            cake_choco * 20 +
            cake_vanilla * 20 +
            juice_orange * 25 +
            juice_watermelon * 25
        )

        st.markdown("---")
        st.subheader(f"💰 Total Amount: ₹{total}")

             payment = st.radio(
            "Choose Payment Method",
            ["GPay", "Cash"]
        )

        if st.button("✅ Place Order"):

            st.success("✅ Order Placed Successfully!")

            st.write(f"Total Amount: ₹{total}")

            st.write(f"Payment Method: {payment}")

            if payment == "GPay":

                st.success("✅ Payment Completed")

                st.write("Status: PAID")

                st.write(f"Amount Received: ₹{total}")

            else:

                st.warning("⏳ Payment Pending")

                st.write(
                    "Student can bring cash tomorrow or parent may pay at the counter."
                )

                st.write("Status: PAYMENT PENDING")

                st.write(f"Amount Due: ₹{total}")
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

            st.success("✅ Access Granted")
            st.subheader("Admin Dashboard")

            st.metric("Today's Orders", "0")
            st.metric("Revenue", "₹0")
        st.markdown("---")

st.subheader("Cash Payment Verification")

student_name = st.text_input(
    "Student Name (Cash Payment)"
)

amount_due = st.number_input(
    "Amount Received",
    min_value=0
)

if st.button("Mark As Paid"):

    st.success(
        f"Payment received from {student_name}"
    )

    st.success(
        f"₹{amount_due} marked as PAID"
    )


        else:
            st.error("❌ Invalid Credentials")
