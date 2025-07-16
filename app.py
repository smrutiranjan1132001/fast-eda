import streamlit as st
import pandas as pd
from utils import eda_utils, feature_utils, viz_utils, llm_agent

# 🎨 Page Config
st.set_page_config(page_title="AI-Driven Data Explorer", layout="wide")

# 📁 Upload File
st.sidebar.header("📂 Upload Your CSV")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

# 🚦 Tabs
tabs = st.sidebar.radio("🔍 Explore", [
    "Data Preview",
    "Basic EDA",
    "Feature Selection",
    "Data Visualizations",
    "Pie Chart",
    "Custom Chart",
    "Interactive Graph",
    "Ask AI"
])

# 🧠 Load Dataset
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success(f"Loaded: {uploaded_file.name}")

    if tabs == "Data Preview":
        st.title("📊 Data Preview")
        st.dataframe(df.head())

    elif tabs == "Basic EDA":
        st.title("📌 Basic EDA")
        eda_utils.show_basic_eda(df)

    elif tabs == "Feature Selection":
        st.title("🧮 Feature Selection")
        feature_utils.select_features(df)

    elif tabs == "Data Visualizations":
        st.title("📈 Quick Visualizations")
        viz_utils.show_charts(df)

    elif tabs == "Pie Chart":
        st.title("🥧 Pie Chart")
        viz_utils.show_pie_chart(df)

    elif tabs == "Custom Chart":
        st.title("📊 Custom Seaborn Chart")
        viz_utils.plot_custom_chart(df)

    elif tabs == "Interactive Graph":
        st.title("📊 Interactive Plotly Chart")
        viz_utils.plot_interactive_chart(df)

    elif tabs == "Ask AI":
        st.title("🤖 Ask AI About Your Data")
        query = st.text_area("Type your question here:")
        if st.button("Generate Insight"):
            response = llm_agent.ask_question(df, query)
            st.success(response)

else:
    st.markdown("### 👋 Welcome to the **AI-Driven Data Explorer**")
    st.markdown("Upload a CSV file from the sidebar to get started!")
