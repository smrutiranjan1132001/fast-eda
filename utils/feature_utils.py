import streamlit as st
from sklearn.feature_selection import mutual_info_classif
import pandas as pd

def select_features(df):
    target = st.selectbox("Select target column", df.columns)
    if target:
        X = df.drop(columns=[target])
        y = df[target]
        numeric_cols = X.select_dtypes(include='number')
        mi = mutual_info_classif(numeric_cols.fillna(0), y)
        scores = pd.Series(mi, index=numeric_cols.columns)
        st.write("Top Features by Mutual Info:")
        st.dataframe(scores.sort_values(ascending=False))
