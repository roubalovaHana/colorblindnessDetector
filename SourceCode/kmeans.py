import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np


def group_colors(image, plot=False):
    # get rid of duplicate colors
    pixels = list(set(image.convert('RGB').getdata()))
    colors = np.array(pixels)

    kmeans = KMeans(n_clusters=20, random_state=0).fit(colors)
    centers = np.array(kmeans.cluster_centers_.astype("uint8"))

    # visualize
    if plot:
        for center in centers:
            # to visualize, colors must have values between 0 and 1
            center = center / 255
            # convert to tuple so that plt sees it as one color
            plt.imshow([[tuple(center)]])
            plt.show()
    return centers
