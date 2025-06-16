import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------- LOGIN PAGE -------------------- #

# Hardcoded login credentials
USER_CREDENTIALS = {
    "admin": "admin123"
}

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

def login():
    st.title("🔐 Login to Medicine Dashboard")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.success(f"Welcome {username}!")
            st.session_state.authenticated = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Invalid username or password")

# If not authenticated, show login page
if not st.session_state.authenticated:
    login()
    st.stop()

# -------------------- MAIN DASHBOARD -------------------- #

st.set_page_config(page_title='Medicine Reviews Dashboard', layout='wide')

# Load data
df = pd.read_csv('Medicine_Details.csv')

# Title
st.title("💊 Medicine Review Analysis Dashboard")

# Sidebar filters
st.sidebar.header("🔍 Filters")
medicine_filter = st.sidebar.text_input("Search Medicine Name")
manufacturer_filter = st.sidebar.selectbox("Select Manufacturer", ["All"] + sorted(df['Manufacturer'].unique().tolist()))
min_excellent = st.sidebar.slider("Minimum Excellent Review %", 0, 100, 30)

# Apply filters
if medicine_filter:
    df = df[df["Medicine Name"].str.contains(medicine_filter, case=False)]

if manufacturer_filter != "All":
    df = df[df["Manufacturer"] == manufacturer_filter]

df = df[df["Excellent Review %"] >= min_excellent]

st.markdown(f"### Showing {len(df)} medicines after applying filters")

# Display table
st.dataframe(df[["Medicine Name", "Manufacturer", "Uses", "Excellent Review %", "Average Review %", "Poor Review %"]])

# Visuals
st.subheader("📊 Review Distribution")
review_sum = df[["Excellent Review %", "Average Review %", "Poor Review %"]].mean()

fig1, ax1 = plt.subplots()
ax1.pie(review_sum, labels=review_sum.index, autopct="%1.1f%%", startangle=90, colors=sns.color_palette("pastel"))
ax1.axis('equal')
st.pyplot(fig1)

# Bar: Top 10 Manufacturers by medicine count
st.subheader("🏭 Top 10 Manufacturers by Number of Medicines")
top_manuf = df['Manufacturer'].value_counts().head(10)

fig2, ax2 = plt.subplots()
sns.barplot(x=top_manuf.values, y=top_manuf.index, palette="viridis", ax=ax2)
ax2.set_xlabel("Number of Medicines")
ax2.set_ylabel("Manufacturer")
st.pyplot(fig2)

# Bar: Top 10 Medicines by Excellent Review %
st.subheader("🌟 Top 10 Medicines by Excellent Review %")
top_meds = df.sort_values(by="Excellent Review %", ascending=False).head(10)

fig3, ax3 = plt.subplots()
sns.barplot(x="Excellent Review %", y="Medicine Name", data=top_meds, palette="magma", ax=ax3)
st.pyplot(fig3)

# Image Viewer
st.subheader("🖼️ Medicine Image Preview")
selected_medicine = st.selectbox("Select a medicine to view image", df["Medicine Name"].unique())
image_url = df[df["Medicine Name"] == selected_medicine]["Image URL"].values[0]
st.image(image_url, caption=selected_medicine, use_column_width=True)

st.markdown("🚀 App built with Streamlit for deployment on Render.")

# Optional: Add a logout button
if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.experimental_rerun()
