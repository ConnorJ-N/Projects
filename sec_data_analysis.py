import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import seaborn as sns
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import plot

class Sec_Data_Analysis():
    
    def __init__(self, data, minmax=True):
        self.data = data
        self.minmax = minmax
        
        if self.minmax is True:
            scaler = MinMaxScaler()
            self.data = scaler.fit_transform(self.data)
    
    def elbow_method(self):
        sum_square_error = []
        K_range = range(2, 10)  # Trying cluster sizes from 2 to 10
        
        for k in K_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(self.data)
            sum_square_error.append(kmeans.inertia_)
        
        # Plot Elbow Method
        plt.figure(figsize=(10, 5))
        plt.plot(K_range, sum_square_error, marker="o", linestyle="-", label="SSE")
        plt.xlabel("Number of Clusters")
        plt.ylabel("Inertia (Sum of Squared Distances)")
        plt.title("Elbow Method for Optimal K")
        plt.legend()
        plt.show()
        
    def cluster_data(self, k=5):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(self.data)
        return cluster_labels, kmeans
    
    def cluster_plot(self, cluster_labels, kmeans, sic=None, company_names=None):
        
        unique_labels = np.unique(cluster_labels)
        color_scale = px.colors.qualitative.Set1
        color_map = {label: color_scale[i % len(color_scale)] for i, label in enumerate(unique_labels)}
        colours = [color_map[label] for label in cluster_labels]
        
        fig = go.Figure()
    
        if sic is not None:
            hover_text = [f"Company: {company} | SIC: {sic_code}" for company, sic_code in zip(company_names, sic)]
        else:
            hover_text = [f"Company: {company}" for company in company_names]
    
        fig.add_trace(go.Scatter(
            x=self.data[:, 0],  # x-axis data
            y=self.data[:, 1],  # y-axis data
            mode='markers',
            marker=dict(color=colours, size=10, opacity=0.7, line=dict(width=1, color='black')),
            text=hover_text,
            hoverinfo='text',
            name="Data Points"))
    
        fig.add_trace(go.Scatter(
            x=kmeans.cluster_centers_[:, 0],
            y=kmeans.cluster_centers_[:, 1],
            mode='markers',
            marker=dict(color='red', size=12, symbol='x', line=dict(width=2, color='black')),
            name="Centroids"))
    
        for label in unique_labels:
            fig.add_trace(go.Scatter(
                x=[None], y=[None],
                mode='markers',
                marker=dict(color=color_map[label], size=10),
                name=f"Cluster {label}"))
    
        fig.update_layout(
            title="K-Means Clustering (2D)",
            xaxis_title="Feature 1",
            yaxis_title="Feature 2",
            showlegend=True)
    
        plot_filename = 'cluster_plot_2d.html'
        plot(fig, filename=plot_filename)