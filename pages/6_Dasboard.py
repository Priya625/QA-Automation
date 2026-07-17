import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

st.title("📊 Project Insights & Analytics Dashboard")

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
    st.error("Could not find a valid survey data file in the project uploads folder.")
    st.stop()

st.markdown("---")

# -----------------------------
# High-Level Metrics Banner
# -----------------------------
st.subheader(f"📈 Executive Overview: {project}")
m1, m2, m3 = st.columns(3)

# Calculate simple insights
total_respondents = len(survey)
total_features = len(survey.columns)
numeric_cols = survey.select_dtypes(include=['number']).columns.tolist()

m1.metric("Total Completed Interviews", f"{total_respondents:,}")
m2.metric("Total Variables Tracked", total_features)
m3.metric("Numeric Data Metrics", len(numeric_cols))

st.markdown("---")

# -----------------------------
# Interactive Visualization Engine
# -----------------------------
st.subheader("🎯 Dynamic Variable Profiler")
st.write("Select any question or column variable below to automatically render its data distribution profile:")

selected_column = st.selectbox(
    "Choose column to visualize:", 
    survey.columns.tolist()
)

if selected_column:
    col_type = survey[selected_column].dtype
    
    # Layout splits: Chart on left, Raw breakdown stats on right
    graph_col, stats_col = st.columns([2, 1])
    
    with graph_col:
        # If the column is numeric with many unique values, treat it as a continuous metric
        if pd.api.types.is_numeric_dtype(col_type) and survey[selected_column].nunique() > 10:
            st.caption(f"Showing distribution trends for numeric variable: **{selected_column}**")
            st.line_chart(survey[selected_column].value_counts().sort_index())
        else:
            # Otherwise, treat it as categorical/discrete and show a frequency bar chart
            st.caption(f"Showing response frequencies for categorical variable: **{selected_column}**")
            value_counts = survey[selected_column].value_counts()
            st.bar_chart(value_counts)
            
    with stats_col:
        st.markdown("**Data Table Summary**")
        # Build a clean frequency distribution matrix table
        freq_df = survey[selected_column].value_counts().reset_index()
        freq_df.columns = ['Response Value', 'Frequency Count']
        freq_df['Percentage Shares'] = (freq_df['Frequency Count'] / total_respondents * 100).round(1).astype(str) + '%'
        st.dataframe(freq_df, use_container_width=True, hide_index=True)

st.markdown("---")

# -----------------------------
# Data Registry Grid View & Export
# -----------------------------
st.subheader("📋 Raw Data Registry Explorer")

with st.expander("🔍 View Complete Underlying Data Spreadsheet Rows", expanded=False):
    st.dataframe(survey, use_container_width=True)

st.markdown("### 💾 Export Engine")
st.write("Download the processed survey sheet direct to your machine local downloads:")

# Convert current dataframe state back to CSV for direct download action
csv_data = survey.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📥 Download Cleaned Project Dataset (.CSV)",
    data=csv_data,
    file_name=f"{project}_Cleaned_Data.csv",
    mime="text/csv",
    type="primary"
)