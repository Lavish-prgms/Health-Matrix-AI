import streamlit as st
import pandas as pd
import random
import time

# Page Setup
st.set_page_config(
    page_title="Health-Matrix AI",
    page_icon="⌚",
    layout="wide"
)

# Professional Medical Styling
st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
background: linear-gradient(180deg,#F5F7FA,#E4ECF7);
}

[data-testid="stHeader"] {
background: rgba(0,0,0,0);
}

[data-testid="stSidebar"] {
background: linear-gradient(180deg,#1E3A5F,#2C5282);
color:white;
}

.card {
background: white;
padding:20px;
border-radius:12px;
margin-bottom:15px;
box-shadow:0px 2px 8px rgba(0,0,0,0.08);
border-left:5px solid #2C5282;
}

h1{
color:#1E3A5F !important;
}

h2,h3{
color:#2C5282 !important;
}

p,label{
color:#2D3748 !important;
}

</style>
""", unsafe_allow_html=True)


# Title
st.title("⌚ Health-Matrix AI")
st.subheader("Smartwatch Based Rural Health Monitoring System")

st.success("⌚ Smartwatch Connected - Live Monitoring Active")

st.markdown("---")


# Sidebar Doctors
st.sidebar.title("👨‍⚕️ Doctor Panel")

doctors = [
"Dr Sharma",
"Dr Singh",
"Dr Verma",
"Dr Mehta",
"Dr Gupta",
"Dr Khan"
]

st.sidebar.subheader("Available Doctors")

for i,doc in enumerate(doctors):
    st.sidebar.write(f"{i+1}. {doc}")


# 8 Patients
patients = [
"Ramesh Kumar",
"Rani Devi",
"Mohan Lal",
"Radha Sharma",
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
        color = "red"

    elif hr > 100 or spo2 < 92 or temp > 100:
        status = "Warning"
        priority = 2
        color = "orange"

    else:
        status = "Normal"
        priority = 3
        color = "green"

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

    st.subheader("⌚ Live Smartwatch Data")

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

    st.subheader("🚨 Emergency Alerts")

    for index,row in df.iterrows():

        if row["Status"] == "Critical":

            st.error(f"Critical : {row['Patient']}")
            st.success(f"Assigned : {row['Doctor']}")

        elif row["Status"] == "Warning":

            st.warning(f"Warning : {row['Patient']}")


# Graph
st.markdown("---")

st.subheader("📈 Live Health Graph")

st.line_chart(df.set_index("Patient")[["HeartRate","Oxygen"]])


# Priority
st.markdown("---")

st.subheader("🚑 Patient Priority")

priority_df = df.sort_values("Priority")

st.dataframe(priority_df, width="stretch")


# Footer
st.markdown("---")

st.caption("Health-Matrix AI | Rural Healthcare Monitoring System | Team Health-Matrix")


# Auto Refresh
time.sleep(5)
st.rerun()
