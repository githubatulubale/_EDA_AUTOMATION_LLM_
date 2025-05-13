import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import tempfile

# Function to Perform EDA and Generate Visualizations
def eda_analysis(file_path):
    df = pd.read_csv(file_path)
    
    # Fill missing values with median for numeric columns
    for col in df.select_dtypes(include=['number']).columns:
        df[col].fillna(df[col].median(), inplace=True)
    
    # Fill missing values with mode for categorical columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col].fillna(df[col].mode()[0], inplace=True)
    
    # Data Summary
    summary = df.describe(include='all').to_string()
    
    # Missing Values
    missing_values = df.isnull().sum().to_string()

    # Generate AI Insights
    insights = generate_ai_insights(summary)
    
    # Generate Data Visualizations
    plot_paths = generate_visualizations(df)
    
    return summary, missing_values, insights, plot_paths

# Placeholder for AI Insights
def generate_ai_insights(df_summary):
    prompt = f"Analyze the dataset summary and provide insights:\n\n{df_summary}"
    # Example with Ollama
    # response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    # return response['message']['content']
    return "AI insights will appear here (placeholder - connect Ollama to enable this)."

# Function to Generate Data Visualizations
def generate_visualizations(df):
    plot_paths = []
    tmpdir = tempfile.mkdtemp()

    # Histograms for Numeric Columns
    for col in df.select_dtypes(include=['number']).columns:
        plt.figure(figsize=(6,4))
        sns.histplot(df[col], bins=30, kde=True, color="blue")
        plt.title(f"Distribution of {col}")
        path = os.path.join(tmpdir, f"{col}_distribution.png")
        plt.savefig(path)
        plot_paths.append(path)
        plt.close()
    
    # Correlation Heatmap (only numeric columns)
    numeric_df = df.select_dtypes(include=['number'])
    if not numeric_df.empty:
        plt.figure(figsize=(8,5))
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title("Correlation Heatmap")
        path = os.path.join(tmpdir, "correlation_heatmap.png")
        plt.savefig(path)
        plot_paths.append(path)
        plt.close()

    return plot_paths

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="InsightIQ", layout="wide")
st.title("InsightIQ")
st.write("Upload any dataset CSV file and get automated EDA insights with AI-powered analysis and visualizations.")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    with st.spinner("Analyzing dataset..."):
        summary, missing_values, insights, plot_paths = eda_analysis(uploaded_file)

        st.success("✅ Data Loaded Successfully!")

        st.subheader("Summary Statistics")
        st.text(summary)

        st.subheader("Missing Values")
        st.text(missing_values)

        st.subheader("AI Insights")
        st.text(insights)

        st.subheader("Data Visualizations")
        cols = st.columns(2)
        for i, img_path in enumerate(plot_paths):
            with cols[i % 2]:
                st.image(img_path, use_column_width=True)
