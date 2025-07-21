import streamlit as st
import pandas as pd
from utils import eda_utils, feature_utils, viz_utils
import streamlit.components.v1 as components

st.set_page_config(page_title="AI-Driven Data Explorer", layout="wide")

st.sidebar.header("📂 Upload Your CSV")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

# Sidebar navigation
tabs = st.sidebar.radio("🔍 Explore", [
    "Data Preview",
    "Basic EDA",
    "Feature Selection",
    "Data Visualizations",
    "Pie Chart",
    "Custom Chart",
    "Interactive Graph",
    #"🤖 Ask AI"
])

# Store DataFrame for chart rendering
preview_data = pd.DataFrame()

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    preview_data = df.head(10)  # limit to avoid performance issues

    st.success("CSV loaded successfully!")

    if tabs == "Data Preview":
        st.title("📊 Data Preview")
        st.dataframe(preview_data)

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
    
    # elif tabs == "🤖 Ask AI":
    #     st.markdown("### 🤖 Ask AI")
    #     question = st.text_area("Ask a question about your dataset:", key="chat_input")
    #     if st.button("Generate Insight", key="ask_ai_button"):
    #         from utils import llm_agent
    #         with st.spinner("Thinking..."):
    #             try:
    #                 response = llm_agent.ask_question(df, question)
    #                 st.success(response)
    #             except Exception as e:
    #                 st.error("Failed to get response from AI.")
    #                 st.exception(e)

else:
    st.markdown("### 👋 Welcome to the **AI-Driven Data Explorer**")
    st.markdown("Upload a CSV file from the sidebar to get started!")

# Floating AI Chat Button
if uploaded_file:
    if "show_chat_popup" not in st.session_state:
        st.session_state.show_chat_popup = False

    st.markdown("""
        <style>
        #chat-toggle-button {
            position: fixed;
            bottom: 25px;
            left: 25px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            font-size: 28px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            z-index: 9999;
        }
        </style>
        <button id="chat-toggle-button" onclick="toggleChat()">🤖</button>
        <script>
            function toggleChat() {
                const streamlitToggleEvent = new Event("chat_toggle_event");
                window.dispatchEvent(streamlitToggleEvent);
            }
            window.addEventListener("chat_toggle_event", function() {
                const input = document.createElement("input");
                input.type = "hidden";
                input.name = "chat_toggle_trigger";
                document.body.appendChild(input);
                input.click();
            });
        </script>
    """, unsafe_allow_html=True)

    if st.button("🤖 Ask AI", key="hidden_toggle_button", help="Hidden AI Chat Toggle Button"):
        st.session_state.show_chat_popup = not st.session_state.show_chat_popup

    if st.session_state.show_chat_popup:
        with st.container():
            st.markdown("""
                <div style='
                    position: fixed;
                    bottom: 100px;
                    left: 25px;
                    background-color: white;
                    width: 300px;
                    padding: 15px;
                    border-radius: 12px;
                    box-shadow: 0px 6px 20px rgba(0,0,0,0.3);
                    z-index: 9998;
                '>
            """, unsafe_allow_html=True)

            st.markdown("### 🤖 Ask AI")
            question = st.text_area("Ask a question about your dataset:", key="chat_input")
            if st.button("Generate Insight", key="ask_ai_button"):
                from utils import llm_agent
                with st.spinner("Thinking..."):
                    try:
                        response = llm_agent.ask_question(df, question)
                        st.success(response)
                    except Exception as e:
                        st.error("Failed to get response from AI.")
                        st.exception(e)

            st.markdown("</div>", unsafe_allow_html=True)