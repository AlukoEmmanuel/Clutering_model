from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
import uvicorn

# Load the saved model
kmeans = joblib.load("model/model.pkl")

# Instantiate the FastAPI app
app = FastAPI(
    title="K-Means Clustering API",
    description="An API for clustering customer data based on annual income and spending score using K-Means clustering",
    version="1.0.0"
)

# Define the input data schema
class CustomerData(BaseModel):
    annual_income: float
    spending_score: float

@app.post(
    "/predict",
    summary="Predict customer cluster",
    description="Predict whether the customer belongs to cluster 0, 1, 2, 3, or 4",
    tags=["prediction"]
)
def predict_cluster(data: CustomerData):
    # Prepare the input for prediction
    input_data = np.array([[data.annual_income, data.spending_score]])
    cluster = kmeans.predict(input_data)[0]

    # Map cluster numbers to labels
    cluster_mapping = {
        0: "Prudent spenders",
        1: "Generous Spenders",
        2: "Extravagant Spenders",
        3: "Wise Spenders",
        4: "Loose Spenders"
    }
    cluster_label = cluster_mapping.get(cluster, "Unknown Cluster")

    return {"cluster": int(cluster), "label": cluster_label}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

