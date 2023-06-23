import base64
import io
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
from sklearn.metrics import silhouette_score


# finds optimal k for KMeans using Silhouette method
def find_optimal_k(colors):
    silhouette_scores = []
    for k in range(2, 10):
        kmeans = KMeans(n_clusters=k, random_state=0).fit(colors)
        score = silhouette_score(colors, kmeans.labels_, sample_size=1000)
        silhouette_scores.append(score)

    return silhouette_scores.index(max(silhouette_scores)) + 2


def group_colors(image):
    # get rid of duplicate colors
    pixels = list(set(image.convert('RGB').getdata()))
    colors = np.array(pixels)
    best_k = find_optimal_k(colors)
    print("best_k: ", best_k)
    kmeans = KMeans(n_clusters=best_k, random_state=0).fit(colors)
    centers = np.array(kmeans.cluster_centers_.astype("uint8"))
    return centers


def visualize_colors(colors):
    plt.scatter(np.arange(colors.shape[0]), np.zeros(colors.shape[0]), color=colors / 255, s=100)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode()
