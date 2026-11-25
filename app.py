import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="MunchMate",
    page_icon="🍽️",
    layout="wide"
)

ORDERS_FILE = "orders.csv"
COLUMNS = [
    "OrderID",
    "StudentName",
    "ClassSection",
    "RollNo",
    "Items",
    "TotalAmount",
    "PaymentMethod",
    "PaymentStatus",
    "DeliveryStatus",
]


def load_orders() -> pd.DataFrame:
    if os.path.exists(ORDERS_FILE):
        df = pd.read_csv(ORDERS_FILE, dtype={"RollNo": str})
        for col in COLUMNS:
            if col not in df.columns:
                df[col] = ""
        return df[COLUMNS]
    return pd.DataFrame(columns=COLUMNS)


def save_orders(df: pd.DataFrame) -> None:
    df.to_csv(ORDERS_FILE, index=False)


def next_order_id(df: pd.DataFrame) -> str:
    if df.empty:
        return "MM0001"
    nums = []
    for oid in df["OrderID"].dropna().astype(str):
        if oid.startswith("MM") and oid[2:].isdigit():
            nums.append(int(oid[2:]))
    nxt = (max(nums) + 1) if nums else len(df) + 1
    return f"MM{nxt:04d}"


# Session State
if "page" not in st.session_state:
    st.session_state.page = "home"

if "student_details_done" not in st.session_state:
    st.session_state.student_details_done = False

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False


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

    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    st.title("🎓 Student Portal")

    tab_order, tab_status = st.tabs(["🛒 Place Order", "🔎 Check Order Status"])

    with tab_order:
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
            if not name.strip() or not roll_no.strip():
                st.warning("Please enter both Student Name and Roll Number.")
            else:
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

            menu_counts = {
                "Classic Veg Burrito": (burrito_classic, 45),
                "Paneer Burrito": (burrito_paneer, 55),
                "Classic Veg Sandwich": (sandwich_classic, 25),
                "Cheese Sandwich": (sandwich_cheese, 35),
                "Chocolate Cake Pop": (cake_choco, 20),
                "Vanilla Cake Pop": (cake_vanilla, 20),
                "Orange Juice": (juice_orange, 25),
                "Watermelon Juice": (juice_watermelon, 25),
            }

            total = sum(qty * price for qty, price in menu_counts.values())
            items_summary = ", ".join(
                f"{item} x{qty}" for item, (qty, _) in menu_counts.items() if qty > 0
            )

            st.markdown("---")
            st.subheader(f"💰 Total Amount: ₹{total}")

            payment = st.radio(
                "Choose Payment Method",
                ["GPay", "Cash"]
            )

            if st.button("✅ Place Order"):
                if total == 0:
                    st.error("Please select at least one item before placing an order.")
                else:
                    orders_df = load_orders()
                    order_id = next_order_id(orders_df)
                    pay_status = "PAID" if payment == "GPay" else "PAYMENT PENDING"

                    new_row = pd.DataFrame([{
                        "OrderID": order_id,
                        "StudentName": name.strip(),
                        "ClassSection": f"{class_name}-{section}",
                        "RollNo": roll_no.strip(),
                        "Items": items_summary,
                        "TotalAmount": total,
                        "PaymentMethod": payment,
                        "PaymentStatus": pay_status,
                        "DeliveryStatus": "PENDING",
                    }])

                    updated_df = pd.concat([orders_df, new_row], ignore_index=True)
                    save_orders(updated_df)

                    st.success(f"✅ Order Placed Successfully! Order ID: {order_id}")
                    st.write(f"Items: {items_summary}")
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

    with tab_status:
        st.subheader("Check Your Order & Payment Status")
        lookup = st.text_input("Enter your Order ID (e.g., MM0001) or Student Name")
        if lookup.strip():
            orders_df = load_orders()
            mask = (
                orders_df["OrderID"].astype(str).str.lower() == lookup.strip().lower()
            ) | (
                orders_df["StudentName"].astype(str).str.lower().str.contains(lookup.strip().lower(), na=False)
            )
            matches = orders_df[mask]
            if matches.empty:
                st.info("No matching orders found yet.")
            else:
                st.dataframe(matches[["OrderID", "StudentName", "Items", "TotalAmount", "PaymentMethod", "PaymentStatus", "DeliveryStatus"]], use_container_width=True)


# ADMIN PAGE
elif st.session_state.page == "admin":

    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    st.title("🔒 Admin Portal")

    if not st.session_state.admin_logged_in:

        password = st.text_input(
            "Enter Passcode",
            type="password"
        )

        secret = st.text_input(
            "Enter Secret Code",
            type="password"
        )

        if st.button("Login"):
        if st.button("Login"):
            admin_pass = st.secrets.get("admin", {}).get("passcode", "AluSamDhwSri")
            admin_secret = st.secrets.get("admin", {}).get("secret_code", "ADSS")

            if password == admin_pass and secret == admin_secret:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("❌ Invalid Credentials")

    else:

        if st.button("Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()

        st.success("✅ Access Granted")
        st.subheader("Admin Dashboard")

        orders_df = load_orders()
        total_orders = len(orders_df)
        paid_revenue = (
            orders_df.loc[orders_df["PaymentStatus"] == "PAID", "TotalAmount"].sum()
            if not orders_df.empty
            else 0
        )
        pending_cash = (
            orders_df.loc[orders_df["PaymentStatus"] == "PAYMENT PENDING", "TotalAmount"].sum()
            if not orders_df.empty
            else 0
        )

        c1, c2, c3 = st.columns(3)
        c1.metric("Today's Orders", str(total_orders))
        c2.metric("Collected Revenue (PAID)", f"₹{int(paid_revenue)}")
        c3.metric("Pending Cash", f"₹{int(pending_cash)}")

        st.markdown("---")
        st.subheader("📋 All Orders")
        if orders_df.empty:
            st.info("No orders placed yet.")
        else:
            st.dataframe(orders_df, use_container_width=True)

        st.markdown("---")
        st.subheader("💵 Cash Payment Verification")

        pending_df = orders_df[orders_df["PaymentStatus"] == "PAYMENT PENDING"] if not orders_df.empty else pd.DataFrame()

        if pending_df.empty:
            st.success("All orders are paid! No pending cash payments.")
        else:
            options = [
                f"{row['OrderID']} | {row['StudentName']} | Due: ₹{row['TotalAmount']}"
                for _, row in pending_df.iterrows()
            ]
            selected = st.selectbox("Select Pending Cash Order", options)
            selected_id = selected.split(" | ")[0]

            if st.button("Mark As Paid"):
                orders_df.loc[orders_df["OrderID"] == selected_id, "PaymentStatus"] = "PAID"
                save_orders(orders_df)
                st.success(f"✅ Order {selected_id} marked as PAID!")
                st.rerun()
