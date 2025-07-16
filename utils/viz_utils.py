import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

def show_charts(df):
    numeric_cols = df.select_dtypes(include='number').columns
    if len(numeric_cols) >= 2:
        st.write("Correlation Heatmap:")
        corr = df[numeric_cols].corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)
    
    col = st.selectbox("Select column to plot distribution", numeric_cols)
    if col:
        fig, ax = plt.subplots()
        sns.histplot(df[col].dropna(), kde=True, ax=ax)
        st.pyplot(fig)

def show_pie_chart(df):
    cat_cols = df.select_dtypes(include='object').columns.tolist()
    if not cat_cols:
        st.info("No categorical columns available for pie chart.")
        return

    col = st.selectbox("Select column to plot pie chart", cat_cols)
    if col:
        value_counts = df[col].value_counts().head(10)  # Limit to top 10 for clarity
        fig, ax = plt.subplots()
        ax.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures the pie is circular.
        st.pyplot(fig)


def plot_custom_chart(df):

    # Identify column types
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    num_cols = df.select_dtypes(include='number').columns.tolist()

    if not cat_cols or not num_cols:
        st.warning("You need at least one categorical and one numerical column.")
        return

    # Dropdowns for user input
    x_col = st.selectbox("Select X-axis (Categorical)", cat_cols)
    y_col = st.selectbox("Select Y-axis (Numerical)", num_cols)
    chart_type = st.selectbox("Choose chart type", ["Bar Plot", "Box Plot", "Violin Plot", "Strip Plot"])

    if x_col and y_col:
        fig, ax = plt.subplots(figsize=(10, 5))
        if chart_type == "Bar Plot":
            sns.barplot(x=x_col, y=y_col, data=df, ax=ax, estimator='mean', errorbar=None)
        elif chart_type == "Box Plot":
            sns.boxplot(x=x_col, y=y_col, data=df, ax=ax)
        elif chart_type == "Violin Plot":
            sns.violinplot(x=x_col, y=y_col, data=df, ax=ax)
        elif chart_type == "Strip Plot":
            sns.stripplot(x=x_col, y=y_col, data=df, ax=ax, jitter=True)

        plt.xticks(rotation=45)
        st.pyplot(fig)

def plot_interactive_chart(df):

    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    num_cols = df.select_dtypes(include='number').columns.tolist()

    if not cat_cols or not num_cols:
        st.warning("You need at least one categorical and one numerical column.")
        return

    x_col = st.selectbox("Select X-axis for (Categorical)", cat_cols)
    y_col = st.selectbox("Select Y-axis for (Numerical)", num_cols)
    agg_func = st.selectbox("Aggregation function", ["mean", "sum", "count", "max", "min"])
    chart_type = st.selectbox("Chart Type", ["Bar", "Box", "Violin", "Strip"])

    # 🔍 Optional: Filter rows based on selected column values
    filter_col = st.selectbox("Optional Filter Column", cat_cols)
    filter_vals = st.multiselect("Select values to include", df[filter_col].unique())

    filtered_df = df.copy()
    if filter_vals:
        filtered_df = df[df[filter_col].isin(filter_vals)]

    # ⚙️ Perform groupby aggregation
    if agg_func in ["mean", "sum", "max", "min", "count"]:
        grouped_df = (
            filtered_df
            .groupby(x_col)[y_col]
            .agg(agg_func)
            .reset_index()
            .rename(columns={y_col: f"{agg_func}_{y_col}"})
        )

    # 📈 Create Plotly chart
    fig = None
    if chart_type == "Bar":
        fig = px.bar(grouped_df, x=x_col, y=grouped_df.columns[1], title=f"{agg_func} of {y_col} by {x_col}")
    elif chart_type == "Box":
        fig = px.box(filtered_df, x=x_col, y=y_col)
    elif chart_type == "Violin":
        fig = px.violin(filtered_df, x=x_col, y=y_col, box=True, points="all")
    elif chart_type == "Strip":
        fig = px.strip(filtered_df, x=x_col, y=y_col)

    if fig:
        fig.update_layout(xaxis_title=x_col, yaxis_title=y_col, title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)
