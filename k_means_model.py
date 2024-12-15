import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import joblib
# import numpy as np
# Load and preprocess data
df = pd.read_csv("data/data_clustering.csv")
print(df.head())
# Assign values to x
x = df.iloc[:, :].values
print(x)
print(x.shape)

# using the elbow method to find the optimal number of clusters
wcss=[]
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(x)
    wcss.append(kmeans.inertia_)

# Plot the Elbow Graph
plt.plot(range(1, 11), wcss, marker='o', linestyle='--', color='b')
plt.title('Elbow Method for Optimal Clusters')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.show()

# Training the k-Means model on the dataset
kmeans = KMeans(n_clusters=5, init='k-means++', random_state=42)
y_pred = kmeans.fit_predict(x)
# save the trained model
joblib.dump(kmeans, "model/model.pkl")
# Prediction
plt.scatter(x[y_pred == 0, 0], x[y_pred ==0, 1], s = 100,  c = "red",label = "Prudent spenders")
plt.scatter(x[y_pred == 1, 0], x[y_pred ==1, 1], s = 100,  c = "blue",label = "Generous Spenders")
plt.scatter(x[y_pred == 2, 0], x[y_pred ==2, 1], s = 100,  c = "green",label = "Extravagant Spenders")
plt.scatter(x[y_pred == 3, 0], x[y_pred ==3, 1], s = 100,  c = "cyan",label = "Wise Spenders")
plt.scatter(x[y_pred == 4, 0], x[y_pred ==4, 1], s = 100,  c = "magenta",label = "Loose Spenders")
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s = 300, c = "yellow", label = "centroids" )
plt.title("clusters of customers")
plt.xlabel("Annual income k$")
plt.ylabel("spending score  (1-100)")
plt.legend()
plt.show()
