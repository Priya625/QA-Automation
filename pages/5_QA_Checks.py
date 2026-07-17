import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

st.title("🛡️ QA Automated Quality Checks")

# 1. Check for active session project
project = st.session_state.get("current_project")

if project is None:
    st.error("No active project found. Please create or open a project first.")
    st.stop()

# 2. Locate and load the active project survey data
folder = os.path.join("uploads", project)
if not os.path.exists(folder):
    st.error(f"Project directory 'uploads/{project}' does not exist.")
    st.stop()

files = os.listdir(folder)
survey = None

for f in files:
    if "quota" in f.lower():
        continue  # Skip quota template file
    if f.endswith(".csv"):
        survey = pd.read_csv(os.path.join(folder, f))
        break
    elif f.endswith(".xlsx"):
        survey = pd.read_excel(os.path.join(folder, f))
        break

if survey is None:
    st.error("Could not find a valid survey data file (.csv or .xlsx) in the project uploads folder.")
    st.stop()

st.markdown("---")
st.subheader(f"Data Engine Audit Summary for: **{project}**")
st.info(f"Loaded dataset successfully containing **{survey.shape[0]}** rows and **{survey.shape[1]}** columns.")

# 3. Setup QA Parameters Interface
st.markdown("### ⚙️ Configure QA Sweep Criteria")
col1, col2 = st.columns(2)

with col1:
    id_col = st.selectbox(
        "Identify Respondent ID column (for duplicate key checks):", 
        survey.columns.tolist()
    )

with col2:
    # Filter only numeric columns to find duration metrics
    numeric_cols = survey.select_dtypes(include=['number']).columns.tolist()
    duration_col = st.selectbox(
        "Identify Duration/LOI column (Optional - for speeder flags):", 
        ["None"] + numeric_cols
    )

# Track execution state cleanly in Streamlit to avoid screen reset bugs
if "qa_executed" not in st.session_state:
    st.session_state["qa_executed"] = False

if st.button("🚀 Run QA Automation Suite", type="primary"):
    st.session_state["qa_executed"] = True

# 4. Display Results Dashboard once the user clicks "Run"
if st.session_state["qa_executed"]:
    st.markdown("---")
    st.markdown("### 📊 Automated Quality Report Summary")
    
    # Execution Logic 1: Find Duplicates
    duplicates = survey[survey.duplicated(subset=[id_col], keep=False)]
    num_dupes = duplicates.shape[0]
    
    # Execution Logic 2: Missing Matrix
    missing_counts = survey.isnull().sum()
    total_missing = missing_counts.sum()
    
    # Visual Metric Badges
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Records Evaluated", len(survey))
    
    m2.metric(
        label="Duplicate Rows Found", 
        value=num_dupes, 
        delta=f"-{num_dupes} flags" if num_dupes > 0 else "0 flags", 
        delta_color="inverse" if num_dupes > 0 else "normal"
    )
    
    m3.metric(
        label="Total Empty Data Cells", 
        value=total_missing, 
        delta=f"-{total_missing} cells" if total_missing > 0 else "0 cells", 
        delta_color="inverse" if total_missing > 0 else "normal"
    )
    
    # Collapsible Detailed Inspections
    with st.expander("🔍 Duplicate ID Registry Detail", expanded=True):
        if num_dupes > 0:
            st.warning(f"Attention required: Found {num_dupes} matching record entries on the unique key.")
            st.dataframe(duplicates)
        else:
            st.success("Clean Pass: All Respondent IDs represent distinctly unique entries.")
            
    with st.expander("📉 Missing Field Matrix Breakdown", expanded=False):
        if total_missing > 0:
            missing_df = missing_counts[missing_counts > 0].reset_index()
            missing_df.columns = ['Column Name/Variable', 'Missing Cell Count']
            st.dataframe(missing_df)
        else:
            st.success("Clean Pass: Complete matrix stability. No null values found across variables.")

    # Execution Logic 3: Speeder Thresholding (Evaluated at < 40% of survey sample median speed)
    if duration_col != "None":
        with st.expander("⏱️ Interview Completion Speed/LOI Anomalies", expanded=True):
            median_time = survey[duration_col].median()
            speeder_threshold = median_time * 0.4
            speeders = survey[survey[duration_col] < speeder_threshold]
            
            st.write(f"Dataset Median Interview Duration: **{median_time:.2f}** units.")
            st.write(f"Automated Speeder Guardrail limit (40% of median): **{speeder_threshold:.2f}** units.")
            
            if len(speeders) > 0:
                st.error(f"Flagged Alert: **{len(speeders)}** respondents completed the instrument too rapidly.")
                st.dataframe(speeders)
            else:
                st.success("Clean Pass: No interview response speeds broke lower control speed boundaries.")

    st.markdown("---")
    
    # 5. Route to Final Dashboard Screen
    if st.button("Proceed to Output Dashboard ➡️"):
        # Explicitly targets your '6_Dasboard.py' file (matching the unique spelling in your sidebar structure)
        st.switch_page("pages/6_Dasboard.py")