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

for f in files:

    if f.endswith(".csv"):

        survey = pd.read_csv(os.path.join(folder, f))

    elif f.endswith(".xlsx"):

        survey = pd.read_excel(os.path.join(folder, f))

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

    st.switch_page("pages/3_QA_Checks.py")