import streamlit as st

st.set_page_config(page_title="Existing Study",layout="wide")

st.title("📂 Existing Study")

st.markdown("---")

from backend.database import get_projects

projects=get_projects()

project=st.selectbox(

    "Select Project",

    projects

)

sample=st.number_input(

    "Sample Size",

    min_value=1,

    value=100

)

survey=st.file_uploader(

    "Upload Current Data",

    type=["csv","xlsx"]

)

if st.button("Continue"):

    st.success("Ready for QA Checks")