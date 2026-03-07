import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="LandHub", layout="wide")

# ---------------- FILE CHECK ---------------- #

if not os.path.exists("users.csv"):
    pd.DataFrame(columns=["Username","Password"]).to_csv("users.csv", index=False)

# ---------------- SESSION ---------------- #

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "user_logged" not in st.session_state:
    st.session_state.user_logged = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ---------------- NAVBAR ---------------- #

col1, col2, col3, col4, col5 = st.columns([3,2,2,2,2])

with col1:
    st.markdown("### 🌾 LandHub")

with col2:
    if st.button("Home"):
        st.session_state.page = "Home"

with col3:
    if st.button("Real Estate"):
        st.session_state.page = "Properties"

with col4:
    if st.button("Tractor Services"):
        st.session_state.page = "Tractors"

with col5:
    if st.button("Favorites"):
        st.session_state.page = "Favorites"

page = st.session_state.page

st.write("---")

# ---------------- USER LOGIN / SIGNUP ---------------- #

st.sidebar.title("👤 User Account")

option = st.sidebar.selectbox("Choose Option", ["Login", "Sign Up"])

if option == "Sign Up":

    new_user = st.sidebar.text_input("Create Username")
    new_pass = st.sidebar.text_input("Create Password", type="password")

    if st.sidebar.button("Register"):

        users = pd.read_csv("users.csv")
        users.columns = users.columns.str.strip()

        if new_user in users["Username"].values:
            st.sidebar.error("Username already exists")

        else:
            new_data = pd.DataFrame([[new_user, new_pass]], columns=["Username","Password"])
            new_data.to_csv("users.csv", mode="a", header=False, index=False)

            st.sidebar.success("Account created! Please login.")

if option == "Login":

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):

        users = pd.read_csv("users.csv")
        users.columns = users.columns.str.strip()

        # remove spaces
        users["Username"] = users["Username"].astype(str).str.strip()
        users["Password"] = users["Password"].astype(str).str.strip()

        username = username.strip()
        password = password.strip()

        user = users[
            (users["Username"] == username) &
            (users["Password"] == password)
        ]

        if not user.empty:
            st.session_state.user_logged = True
            st.session_state.username = username
            st.sidebar.success(f"Welcome {username}")
        else:
            st.sidebar.error("Invalid login")

if st.session_state.user_logged:

    st.sidebar.write(f"Logged in as: **{st.session_state.username}**")

    if st.sidebar.button("Logout"):
        st.session_state.user_logged = False
        st.session_state.username = ""

# ---------------- HOME ---------------- #

if page == "Home":

    st.title("🏡 Real Estate & 🚜 Tractor Booking Platform")

    st.markdown("""
    <div style="text-align:center;padding:40px;background:#f5f7fa;border-radius:10px;">
    <h2>Find Properties & Nearby Tractor Services</h2>
    <p>Everything You Need — Homes, Land & Tractors!</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🏡 Properties Listed", "100+")

    with col2:
        st.metric("🚜 Tractors Available", "50+")

    with col3:
        st.metric("😊 Happy Clients", "500+")

# ---------------- TRACTORS ---------------- #

elif page == "Tractors":

    st.header("🚜 Tractor NearBy")

    df = pd.read_csv("tractors.csv")
    df.columns = df.columns.str.strip()

    location = st.text_input("Search by Location")

    if location:
        df = df[df["Location"].str.contains(location, case=False, na=False)]

    cols = st.columns(3)

    for i, row in df.iterrows():

        with cols[i % 3]:

            st.subheader(row.get("TractorType", "Tractor"))

            st.write("👤 Owner:", row.get("Owner", "N/A"))
            st.write("📍 Location:", row.get("Location", "N/A"))
            st.write("🛠 Service:", row.get("Service", "N/A"))
            st.write("🟢 Availability:", row.get("Availability", "N/A"))

            phone = str(row.get("Contact", ""))

            if phone:
                st.markdown(f"[📞 WhatsApp Owner](https://wa.me/{phone})")

            map_location = row.get("Location", "")

            if map_location:
                st.markdown(f"[📍 View Location](https://www.google.com/maps/search/{map_location})")

            if st.button(f"❤️ Save Tractor {i}"):

                st.session_state.favorites.append({
                    "type": "Tractor",
                    "location": row.get("Location"),
                    "owner": row.get("Owner")
                })

                st.success("Saved to favorites!")

# ---------------- PROPERTIES ---------------- #

elif page == "Properties":

    st.header("🏡 Farm Properties")

    df = pd.read_csv("properties.csv")
    df.columns = df.columns.str.strip()

    location = st.text_input("Search Property Location")

    if location:
        df = df[df["Location"].str.contains(location, case=False, na=False)]

    cols = st.columns(3)

    for i, row in df.iterrows():

        with cols[i % 3]:

            image_name = row.get("Image", "")
            image_path = f"images/{image_name}"

            if image_name and os.path.exists(image_path):
                st.image(image_path, use_container_width=True)

            st.write("📍 Location:", row.get("Location"))
            st.write("💰 Price:", row.get("Price", "N/A"))
            st.write("📞 Contact:", row.get("Contact", "N/A"))

            phone = str(row.get("Contact", ""))

            if phone:
                st.markdown(f"[📞 WhatsApp Owner](https://wa.me/{phone})")

            map_location = row.get("Location", "")

            if map_location:
                st.markdown(f"[📍 View Location](https://www.google.com/maps/search/{map_location})")

            if st.button(f"❤️ Save Property {i}"):

                st.session_state.favorites.append({
                    "type": "Property",
                    "location": row.get("Location"),
                    "price": row.get("Price")
                })

                st.success("Saved to favorites!")

# ---------------- FAVORITES ---------------- #

elif page == "Favorites":

    st.header("❤️ Saved Listings")

    if len(st.session_state.favorites) == 0:
        st.info("No favorites yet")

    for item in st.session_state.favorites:

        if item["type"] == "Property":
            st.write(f"🏡 Property - {item['location']} | 💰 {item['price']}")

        if item["type"] == "Tractor":
            st.write(f"🚜 Tractor - {item['location']} | Owner: {item['owner']}")

# ---------------- ADD PROPERTY ---------------- #

if st.session_state.user_logged:

    st.sidebar.write("---")

    if st.sidebar.button("➕ Add Property"):

        st.header("Add Property")

        owner = st.text_input("Owner Name")
        location = st.text_input("Location")
        price = st.text_input("Price")
        contact = st.text_input("Contact Number")

        image_file = st.file_uploader("Upload Property Image")

        image_name = ""

        if image_file is not None:

            if not os.path.exists("images"):
                os.makedirs("images")

            image_name = image_file.name

            with open(os.path.join("images", image_name), "wb") as f:
                f.write(image_file.getbuffer())

        if st.button("Add Property"):

            new_data = pd.DataFrame([{
                "Owner": owner,
                "Location": location,
                "Price": price,
                "Contact": contact,
                "Image": image_name
            }])

            new_data.to_csv("properties.csv", mode="a", header=False, index=False)

            st.success("Property Added Successfully!")

# ---------------- ADD TRACTOR ---------------- #

if st.session_state.user_logged:

    if st.sidebar.button("➕ Add Tractor"):

        st.header("Add Tractor Service")

        owner = st.text_input("Owner Name")
        tractor = st.text_input("Tractor Type")
        location = st.text_input("Location")
        service = st.text_input("Service Type")
        availability = st.selectbox("Availability", ["Available", "Busy"])
        contact = st.text_input("Contact Number")

        if st.button("Add Tractor"):

            new_data = pd.DataFrame([{
                "Owner": owner,
                "TractorType": tractor,
                "Location": location,
                "Service": service,
                "Availability": availability,
                "Contact": contact
            }])

            new_data.to_csv("tractors.csv", mode="a", header=False, index=False)

            st.success("Tractor Service Added Successfully!")