import pandas as pd


def load_file(uploaded_file):

    if uploaded_file.name.endswith(".csv"):

        df=pd.read_csv(uploaded_file)

    else:

        df=pd.read_excel(uploaded_file)

    return df