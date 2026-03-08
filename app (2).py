import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="LandHub", layout="wide")

# ---------- FILE CHECK ----------
for file, cols in {
    "users.csv":["Username","Password"],
    "properties.csv":["Owner","Location","Price","Contact","Image"],
    "tractors.csv":["Owner","TractorType","Location","Service","Availability","Contact"]
}.items():
    if not os.path.exists(file):
        pd.DataFrame(columns=cols).to_csv(file,index=False)

# ---------- SESSION ----------
if "page" not in st.session_state:
    st.session_state.page="Home"

if "favorites" not in st.session_state:
    st.session_state.favorites=[]

if "logged" not in st.session_state:
    st.session_state.logged=False

if "username" not in st.session_state:
    st.session_state.username=""

# ---------- NAVBAR ----------
col1,col2,col3,col4,col5 = st.columns([3,2,2,2,2])

with col1:
    st.markdown("## 🌾 LandHub")

with col2:
    if st.button("Home"):
        st.session_state.page="Home"

with col3:
    if st.button("Real Estate"):
        st.session_state.page="Properties"

with col4:
    if st.button("Tractor Services"):
        st.session_state.page="Tractors"

with col5:
    if st.button("Favorites"):
        st.session_state.page="Favorites"

page=st.session_state.page
st.write("---")

# ---------- USER LOGIN ----------
st.sidebar.title("👤 User Account")
option=st.sidebar.selectbox("Choose Option",["Login","Sign Up"])

if option=="Sign Up":

    new_user=st.sidebar.text_input("Username")
    new_pass=st.sidebar.text_input("Password",type="password")

    if st.sidebar.button("Register"):

        users=pd.read_csv("users.csv")

        if new_user in users["Username"].values:
            st.sidebar.error("Username already exists")

        else:
            pd.DataFrame([[new_user,new_pass]],
            columns=["Username","Password"]).to_csv(
            "users.csv",mode="a",header=False,index=False)

            st.sidebar.success("Account Created")

if option=="Login":

    username=st.sidebar.text_input("Username")
    password=st.sidebar.text_input("Password",type="password")

    if st.sidebar.button("Login"):

        users=pd.read_csv("users.csv")

        user=users[
            (users["Username"].astype(str).str.strip()==username.strip()) &
            (users["Password"].astype(str).str.strip()==password.strip())
        ]

        if not user.empty:
            st.session_state.logged=True
            st.session_state.username=username
            st.sidebar.success(f"Welcome {username}")

        else:
            st.sidebar.error("Invalid Login")

if st.session_state.logged:

    st.sidebar.write(f"Logged in as **{st.session_state.username}**")

    if st.sidebar.button("Logout"):
        st.session_state.logged=False
        st.session_state.username=""

# ---------- HOME ----------
if page=="Home":

    st.title("🏡 Real Estate & 🚜 Tractor Platform")

    st.markdown("""
    <div style="background:#f5f7fa;padding:30px;border-radius:10px;text-align:center">
    <h2>Find Land, Houses & Tractor Services Near You</h2>
    </div>
    """,unsafe_allow_html=True)

    st.image([
        "House1 (1).jpeg",
        "Land1 (1).jpg",
        "Appartment2 (1).jpg"
    ])

    col1,col2,col3=st.columns(3)

    col1.metric("🏡 Properties","100+")
    col2.metric("🚜 Tractors","50+")
    col3.metric("😊 Clients","500+")

# ---------- TRACTORS ----------
elif page=="Tractors":

    st.header("🚜 Tractor Services")

    df=pd.read_csv("tractors.csv")

    search=st.text_input("Search Location")

    if search:
        df=df[df["Location"].str.contains(search,case=False,na=False)]

    cols=st.columns(3)

    for i,row in df.iterrows():

        with cols[i%3]:

            st.subheader(row["TractorType"])

            st.write("👤 Owner:",row["Owner"])
            st.write("📍 Location:",row["Location"])
            st.write("🛠 Service:",row["Service"])
            st.write("🟢 Availability:",row["Availability"])

            phone=str(row["Contact"])

            st.markdown(f"[📞 WhatsApp](https://wa.me/{phone})")

            st.map(pd.DataFrame({
                "lat":[17.3850],
                "lon":[78.4867]
            }))

            if st.button(f"❤️ Save Tractor {i}"):

                st.session_state.favorites.append({
                    "type":"Tractor",
                    "location":row["Location"],
                    "owner":row["Owner"]
                })

# ---------- PROPERTIES ----------
elif page=="Properties":

    st.header("🏡 Farm Properties")

    df=pd.read_csv("properties.csv")

    st.write(f"Total Properties: **{len(df)}**")

    search=st.text_input("Search Location")

    price_filter=st.selectbox(
        "Price Filter",
        ["All","Below 10L","10L-20L","Above 20L"]
    )

    if search:
        df=df[df["Location"].str.contains(search,case=False,na=False)]

    cols=st.columns(3)

    for i,row in df.iterrows():

        with cols[i%3]:

            st.markdown("""
            <div style="background:#fafafa;padding:15px;border-radius:10px;
            box-shadow:0px 2px 6px rgba(0,0,0,0.1)">
            """,unsafe_allow_html=True)

            image=row["Image"]

            if image!="" and os.path.exists(image):
                st.image(image,use_container_width=True)

            else:
                st.image("https://via.placeholder.com/400x250")

            st.subheader(row["Location"])

            st.write("💰",row["Price"])
            st.write("📞",row["Contact"])

            phone=str(row["Contact"])

            st.markdown(f"[📞 WhatsApp](https://wa.me/{phone})")

            st.markdown(
            f"[📍 Map](https://www.google.com/maps/search/{row['Location']})"
            )

            if st.button(f"❤️ Save Property {i}"):

                st.session_state.favorites.append({
                    "type":"Property",
                    "location":row["Location"],
                    "price":row["Price"]
                })

            st.markdown("</div>",unsafe_allow_html=True)

# ---------- FAVORITES ----------
elif page=="Favorites":

    st.header("❤️ Favorites")

    if len(st.session_state.favorites)==0:
        st.info("No saved items")

    for item in st.session_state.favorites:

        if item["type"]=="Property":
            st.write(f"🏡 {item['location']} | 💰 {item['price']}")

        if item["type"]=="Tractor":
            st.write(f"🚜 {item['location']} | Owner {item['owner']}")

# ---------- ADD PROPERTY ----------
if st.session_state.logged:

    st.sidebar.write("---")

    if st.sidebar.button("➕ Add Property"):

        st.header("Add Property")

        owner=st.text_input("Owner")
        location=st.text_input("Location")
        price=st.text_input("Price")
        contact=st.text_input("Contact")

        image=st.file_uploader("Upload Image")

        image_name=""

        if image:

            if not os.path.exists("images"):
                os.makedirs("images")

            image_name=image.name

            with open(os.path.join("images",image_name),"wb") as f:
                f.write(image.getbuffer())

        if st.button("Submit"):

            pd.DataFrame([{
                "Owner":owner,
                "Location":location,
                "Price":price,
                "Contact":contact,
                "Image":image_name
            }]).to_csv("properties.csv",mode="a",header=False,index=False)

            st.success("Property Added")

# ---------- ADD TRACTOR ----------
if st.session_state.logged:

    if st.sidebar.button("➕ Add Tractor"):

        st.header("Add Tractor")

        owner=st.text_input("Owner")
        tractor=st.text_input("Tractor Type")
        location=st.text_input("Location")
        service=st.text_input("Service")
        availability=st.selectbox("Availability",["Available","Busy"])
        contact=st.text_input("Contact")

        if st.button("Submit Tractor"):

            pd.DataFrame([{
                "Owner":owner,
                "TractorType":tractor,
                "Location":location,
                "Service":service,
                "Availability":availability,
                "Contact":contact
            }]).to_csv("tractors.csv",mode="a",header=False,index=False)

            st.success("Tractor Added")
