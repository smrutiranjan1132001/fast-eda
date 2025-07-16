import streamlit as st
import pandas as pd

def show_basic_eda(df):
    st.write("Shape:", df.shape)
    st.write("Column Types:", df.dtypes)
    st.write("Missing Values:", df.isnull().sum())
    st.write("Descriptive Stats:")
    st.dataframe(df.describe(include='all'))
