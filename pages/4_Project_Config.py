import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

st.title("Project Configuration")

project = st.session_state.get("current_project")

if project is None:
    st.error("No active project.")
    st.stop()

folder = os.path.join("uploads", project)
files = os.listdir(folder)

survey = None

# FIX 1: Skip the quota file so it doesn't overwrite your survey dataset
for f in files:
    if "quota" in f.lower():
        continue  # Ignore quota templates here
        
    if f.endswith(".csv"):
        survey = pd.read_csv(os.path.join(folder, f))
        break
    elif f.endswith(".xlsx"):
        survey = pd.read_excel(os.path.join(folder, f))
        break

# Safety check in case no survey file was parsed
if survey is None:
    st.error("Could not locate or load the survey data file in the project folder.")
    st.stop()

questions = survey.columns.tolist()

st.subheader("Map Important Questions")

respondent = st.selectbox(
    "Respondent ID",
    questions
)

duration = st.selectbox(
    "Duration Variable",
    questions
)

awareness = st.selectbox(
    "Awareness Question",
    questions
)

consideration = st.selectbox(
    "Consideration Question",
    questions
)

purchase = st.selectbox(
    "Purchase Intent",
    questions
)

if st.button("Save Configuration"):
    st.success("Configuration Saved")
    # FIX 2: Updated to match 5_QA_Checks.py in your sidebar directory
    st.switch_page("pages/5_QA_Checks.py")