import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# App Configuration
st.set_page_config(
    page_title="Customer Insights & Segmentation",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# App Title and Introduction
st.title("🎯 Customer Insights & Segmentation Platform")
st.markdown("""
Welcome to the **Customer Insights Platform**, your go-to tool for understanding customer behavior through K-Means clustering.  
This app provides **actionable insights** by grouping customers into **five distinct segments** based on their annual income and spending score.  
### Benefits of This Tool:
- **Understand Your Customers**: Tailor strategies to each segment.  
- **Increase Revenue**: Target marketing for higher ROI.  
- **Data-Driven Decisions**: Use insights to make smarter business moves.  
""")

# Sidebar Input Section
st.sidebar.header("Single Customer Prediction")
annual_income = st.sidebar.number_input(
    "Annual Income (k$):", min_value=0, max_value=200, step=1, value=15
)
spending_score = st.sidebar.number_input(
    "Spending Score (1-100):", min_value=1, max_value=100, step=1, value=50
)

# Prediction API URL
API_URL = "http://127.0.0.1:8000/predict"  # Replace with your live API endpoint

# Single Prediction
if st.sidebar.button("Predict Customer Segment"):
    input_data = {"annual_income": annual_income, "spending_score": spending_score}
    try:
        response = requests.post(API_URL, json=input_data)
        if response.status_code == 200:
            cluster = response.json()["cluster"]
            cluster_names = {
                1: "Luxury Loyalists",
                2: "Frugal Followers",
                3: "Balanced Buyers",
                4: "Impulsive Shoppers",
                5: "Thrifty Opportunists"
            }
            st.success(f"🎉 The customer belongs to **Cluster {cluster}: {cluster_names[cluster]}**.")
        else:
            st.error("Failed to fetch prediction. Check the API endpoint.")
    except Exception as e:
        st.error(f"Error: {e}")

# Batch Prediction Section
st.markdown("### 📂 Batch Prediction")
uploaded_file = st.file_uploader("Upload a CSV file (with 'Annual Income' and 'Spending Score')", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded Data:")
    st.dataframe(df)

    if "Annual Income" in df.columns and "Spending Score" in df.columns:
        try:
            predictions = []
            for _, row in df.iterrows():
                input_data = {
                    "annual_income": row["Annual Income"],
                    "spending_score": row["Spending Score"]
                }
                response = requests.post(API_URL, json=input_data)
                if response.status_code == 200:
                    predictions.append(response.json()["cluster"])
                else:
                    predictions.append(None)

            df["Cluster"] = predictions
            cluster_names = {
                1: "Luxury Loyalists",
                2: "Frugal Followers",
                3: "Balanced Buyers",
                4: "Impulsive Shoppers",
                5: "Thrifty Opportunists"
            }
            df["Cluster Name"] = df["Cluster"].map(cluster_names)

            st.write("Clustered Data:")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Clustered Data",
                data=csv,
                file_name="customer_segments.csv",
                mime="text/csv"
            )

            st.markdown("### 📊 Cluster Visualization")
            fig = px.scatter(
                df,
                x="Annual Income",
                y="Spending Score",
                color="Cluster Name",
                title="Customer Segmentation Clusters",
                labels={"Cluster Name": "Customer Segment"},
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error processing batch predictions: {e}")
    else:
        st.error("CSV must contain 'Annual Income' and 'Spending Score' columns.")

# Footer
st.markdown("---")
st.markdown("""
**Developed by [Aluko Emmanuel](#)** | Powered by **Streamlit** 🚀  
**Customer Segmentation Names**:
- **Luxury Loyalists**: High-income, high-spending customers.  
- **Frugal Followers**: Low-income, low-spending customers.  
- **Balanced Buyers**: Middle-income, moderate-spending customers.  
- **Impulsive Shoppers**: Trend-driven customers with spontaneous purchases.  
- **Thrifty Opportunists**: Strategic spenders seeking value.  
""")
