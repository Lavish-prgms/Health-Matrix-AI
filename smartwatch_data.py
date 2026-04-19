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

# Session State
if "doctor_assignments" not in st.session_state:
    st.session_state.doctor_assignments = {}

# Dark Professional Styling
st.markdown("""
<style>

.stApp {
background: #F4F6FB;
color:#0F172A;
}

section[data-testid="stSidebar"] {
background: #1E293B;
}

section[data-testid="stSidebar"] * {
color: #F1F5F9 !important;
}

.card {
background: white;
padding:20px;
border-radius:12px;
margin-bottom:15px;
border-left:5px solid #2563EB;
box-shadow: 0 4px 10px rgba(0,0,0,0.08);
color:#0F172A;
}

h1{
color:#0F172A !important;
font-weight:700;
}

h2,h3{
color:#1E293B !important;
font-weight:600;
}

p, label, span {
color:#334155 !important;
font-weight:500;
}

</style>
""", unsafe_allow_html=True)


# Title
st.title("⌚ Health-Matrix AI")
st.subheader("Smartwatch Based Rural Health Monitoring System")

st.success("⌚ Smartwatch Connected - Live Monitoring Active")

st.markdown("---")


# Doctors (Levels)
critical_doctors = [
"Dr Sharma (Emergency)",
"Dr Mehta (ICU)",
"Dr Singh (Critical Care)"
]

highrisk_doctors = [
"Dr Verma",
"Dr Khan",
"Dr Gupta"
]

moderate_doctors = [
"Dr Patel",
"Dr Kumar"
]

normal_doctors = [
"Dr Reddy",
"Dr Das",
"Dr Joshi"
]

all_doctors = critical_doctors + highrisk_doctors + moderate_doctors + normal_doctors


# Sidebar
st.sidebar.title("👨‍⚕️ Doctor Panel")

st.sidebar.subheader("Critical Care")
for d in critical_doctors:
    st.sidebar.write(d)

st.sidebar.subheader("High Risk")
for d in highrisk_doctors:
    st.sidebar.write(d)

st.sidebar.subheader("Moderate")
for d in moderate_doctors:
    st.sidebar.write(d)

st.sidebar.subheader("General")
for d in normal_doctors:
    st.sidebar.write(d)


# Patients
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
waiting_list = []

for i,p in enumerate(patients):

    hr = random.randint(70,140)
    spo2 = random.randint(85,100)
    temp = round(random.uniform(97,103),1)

    # Status Levels
    if hr > 125 or spo2 < 88 or temp > 102:
        status = "Critical"
        priority = 1
        color = "#DC2626"
        doctor_pool = critical_doctors

    elif hr > 110 or spo2 < 92:
        status = "High Risk"
        priority = 2
        color = "#F97316"
        doctor_pool = highrisk_doctors

    elif hr > 95:
        status = "Moderate"
        priority = 3
        color = "#EAB308"
        doctor_pool = moderate_doctors

    else:
        status = "Normal"
        priority = 4
        color = "#059669"
        doctor_pool = normal_doctors


    # Doctor Assignment
    if p in st.session_state.doctor_assignments:
        doctor = st.session_state.doctor_assignments[p]

    else:
        assigned = False

        for d in doctor_pool:
            if d not in st.session_state.doctor_assignments.values():
                doctor = d
                st.session_state.doctor_assignments[p] = doctor
                assigned = True
                break

        if not assigned:
            doctor = "Waiting"
            waiting_list.append(p)

    data.append({
        "S.No": i+1,
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


# Smartwatch Cards
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

        elif row["Status"] == "High Risk":
            st.warning(f"High Risk : {row['Patient']}")

    if waiting_list:
        st.subheader("⏳ Waiting Patients")
        for w in waiting_list:
            st.info(w)


# Graph
st.markdown("---")

st.subheader("📈 Live Health Graph")

st.line_chart(df.set_index("Patient")[["HeartRate","Oxygen"]])


# Priority Table
st.markdown("---")

st.subheader("🚑 Patient Priority")

priority_df = df.sort_values("Priority")


def highlight_status(val):

    if val == "Critical":
        return 'background-color:#FEE2E2;color:#991B1B'

    elif val == "High Risk":
        return 'background-color:#FFF7ED;color:#C2410C'

    elif val == "Moderate":
        return 'background-color:#FEF9C3;color:#854D0E'

    else:
        return 'background-color:#ECFDF5;color:#065F46'


display_df = priority_df.drop(columns=["Color"])

styled_df = display_df.style.applymap(
    highlight_status,
    subset=["Status"]
)

st.dataframe(
    styled_df,
    use_container_width=True,
    height=420
)


# Footer
st.markdown("---")

st.caption("Health-Matrix AI | Smartwatch Based Rural Healthcare Monitoring")


# Auto Refresh
time.sleep(5)
st.rerun()
