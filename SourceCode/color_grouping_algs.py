import numpy as np
from abc import ABC, abstractmethod
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from SourceCode import deltaE_distance_calculator


class ColorGroupingStrategy(ABC):
    """ Abstract base class that defines interface for color grouping strategies"""
    @abstractmethod
    def group_colors(self, colors: np.array, threshold: int) -> np.array:
        pass


class KMeansColorGroupingStrategy(ColorGroupingStrategy):
    """ Represents the K-Means color grouping strategy"""

    def _find_optimal_k(self, colors):
        """
        Finds optimal k for KMeans using Silhouette method
        :param colors: Image colors to cluster
        :return: The optimal value of k
        """
        silhouette_scores = []
        for k in range(2, 10):
            kmeans = KMeans(n_clusters=k, random_state=0).fit(colors)
            score = silhouette_score(colors, kmeans.labels_, sample_size=1000)
            silhouette_scores.append(score)

        return silhouette_scores.index(max(silhouette_scores)) + 2

    def group_colors(self, colors: np.array, threshold) -> np.array:
        """
        Uses the K-Means clustering algorithm to find clusters of colors in the image.
        :param colors: Image colors to cluster
        :param threshold: Unused
        :return: The cluster centers of grouped colors
        """
        best_k = self._find_optimal_k(colors)
        # print("best_k: ", best_k)
        kmeans = KMeans(n_clusters=best_k, random_state=0).fit(colors)
        centers = np.array(kmeans.cluster_centers_.astype("uint8"))
        return centers


class EuclideanDistColorGroupingStrategy(ColorGroupingStrategy):
    """ Represents the Euclidean distance color grouping strategy. """
    def _group_colors(self, colors: np.array, threshold) -> np.array:
        """
        Recursively groups colors based on their Euclidean distances.
        Colors with distances below the threshold are grouped together
        :param colors: Image colors to cluster
        :param threshold: Value determining which colors are close enough to be in single group
        :return: Grouped colors
        """
        if len(colors) > 0:
            distances = np.array(list(np.linalg.norm(colors[0] - color) for color in colors))
            group = colors[distances <= threshold]
            rest = colors[distances > threshold]
            rest_result = self._group_colors(rest, threshold)
            return [group] + rest_result
        return []

    def group_colors(self, colors: np.array, threshold) -> np.array:
        """
        Recursively groups colors based on their Euclidean distances.
        :param colors: Image colors to cluster
        :param threshold: Value determining which colors are close enough to be in single group
        :return: The mean of each group as the representative of each group.
        """
        grouped_colors = self._group_colors(colors, threshold)
        # print("group_count: ", len(grouped_colors))
        return [np.mean(group, axis=0) for group in grouped_colors]


class DeltaEDistColorGroupingStrategy(ColorGroupingStrategy):
    """ represents the DeltaE distance color grouping strategy. """
    def _group_colors(self, colors: np.array, threshold) -> np.array:
        """
        Recursively groups colors based on their DeltaE distances.
        Colors with distances below the threshold are grouped together
        :param colors: Image colors to cluster
        :param threshold: Value determining which colors are close enough to be in single group
        :return: Grouped colors
        """
        if len(colors) > 0:
            distances = cdist(colors[0:1], colors, metric=deltaE_distance_calculator.pairwise_deltaE_distance)[0]
            group = colors[distances <= threshold]
            rest = colors[distances > threshold]
            return [group] + self._group_colors(rest, threshold)
        return []

    def group_colors(self, colors: np.array, threshold) -> np.array:
        """
         Recursively groups colors based on their DeltaE distances.
        :param colors: Image colors to cluster
        :param threshold: Value determining which colors are close enough to be in single group
        :return: The mean of each group as the representative of each group.
        """
        grouped_colors = self._group_colors(colors, threshold)
        # print("group_count: ", len(grouped_colors))
        return [np.mean(group, axis=0) for group in grouped_colors]
