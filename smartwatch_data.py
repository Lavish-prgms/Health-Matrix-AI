import streamlit as st
import pandas as pd
import random
import time

# Page Setup
st.set_page_config(
    page_title="Health-Matrix AI",
    page_icon="🧠",
    layout="wide"
)

# Futuristic Neon Styling
st.markdown("""
<style>

.stApp {
background: linear-gradient(135deg,#020024,#090979,#00d4ff);
}

.card {
background: rgba(255,255,255,0.08);
backdrop-filter: blur(15px);
padding:22px;
border-radius:18px;
margin-bottom:18px;
border:1px solid rgba(255,255,255,0.15);
box-shadow:0 0 20px rgba(0,212,255,0.4);
transition:0.3s;
}

.card:hover{
transform: scale(1.02);
box-shadow:0 0 35px rgba(0,255,255,0.8);
}

h1{
color:#00ffff !important;
text-shadow:0 0 20px #00ffff;
}

h2,h3,h4,p,label{
color:white !important;
}

section[data-testid="stSidebar"] {
background: linear-gradient(180deg,#000428,#004e92);
border-right:1px solid rgba(255,255,255,0.2);
}

</style>
""", unsafe_allow_html=True)


# Title
st.title("🧠 Health-Matrix AI")
st.subheader("AI Powered Smartwatch Healthcare Monitoring")

st.success("⌚ Smartwatch Connected | Live AI Monitoring Active")

st.markdown("---")


# Sidebar Doctors
st.sidebar.title("👨‍⚕️ Doctor Control Center")

doctors = [
"Dr Sharma",
"Dr Singh",
"Dr Verma",
"Dr Mehta",
"Dr Gupta",
"Dr Khan",
"Dr Reddy",
"Dr Patel"
]

st.sidebar.subheader("Available Doctors")

for i,doc in enumerate(doctors):
    st.sidebar.write(f"{i+1}. {doc}")


# Patients
patients = [
"Ramesh Kumar",
"Surbhi",
"Mohan Lal",
"Satyender",
"Sunita Devi",
"Rahul Kumar",
"Anita Sharma",
"Vikas Singh"
]


# Generate Data
data = []

for p in patients:

    hr = random.randint(70,140)
    spo2 = random.randint(85,100)
    temp = round(random.uniform(97,103),1)

    if hr > 120 or spo2 < 88 or temp > 102:
        status = "Critical"
        priority = 1
        color = "#ff0055"

    elif hr > 100 or spo2 < 92 or temp > 100:
        status = "Warning"
        priority = 2
        color = "#ffaa00"

    else:
        status = "Normal"
        priority = 3
        color = "#00ffcc"

    doctor = random.choice(doctors)

    data.append({
        "Patient":p,
        "HeartRate":hr,
        "Oxygen":spo2,
        "Temperature":temp,
        "Status":status,
        "Priority":priority,
        "Doctor":doctor,
        "Color":color
    })


df = pd.DataFrame(data)


# Layout
col1,col2 = st.columns([2,1])


# Smartwatch Data
with col1:

    st.subheader("📡 Live Smartwatch Data")

    for index,row in df.iterrows():

        st.markdown(f"""
        <div class="card">

        <h3>{row['Patient']}</h3>

        ❤️ Heart Rate : {row['HeartRate']} bpm <br>
        🫁 Oxygen : {row['Oxygen']} % <br>
        🌡 Temperature : {row['Temperature']} °F <br>

        <b style="color:{row['Color']}">
        Status : {row['Status']}
        </b>

        </div>
        """, unsafe_allow_html=True)


# Alerts
with col2:

    st.subheader("🚨 AI Emergency Alerts")

    for index,row in df.iterrows():

        if row["Status"] == "Critical":

            st.error(f"🚨 Critical : {row['Patient']}")
            st.success(f"👨‍⚕️ Assigned : {row['Doctor']}")

        elif row["Status"] == "Warning":

            st.warning(f"⚠️ Warning : {row['Patient']}")


# Graph
st.markdown("---")

st.subheader("📈 AI Health Monitoring Graph")

st.line_chart(df.set_index("Patient")[["HeartRate","Oxygen"]])


# Priority
st.markdown("---")

st.subheader("🚑 Patient Priority Queue")

priority_df = df.sort_values("Priority")

st.dataframe(priority_df, width="stretch")


# Footer
st.markdown("---")

st.caption("Health-Matrix AI | Next-Gen Rural Healthcare Monitoring")


# Auto Refresh
time.sleep(5)
st.rerun()
