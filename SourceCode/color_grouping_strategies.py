from abc import abstractmethod, ABC
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


class ColorGroupingStrategy(ABC):

    @abstractmethod
    def group_colors(self, colors: np.array):
        pass


class KMeansColorGroupingStrategy(ColorGroupingStrategy):

    # finds optimal k for KMeans using Silhouette method
    def _find_optimal_k(self, colors):
        silhouette_scores = []
        for k in range(2, 10):
            kmeans = KMeans(n_clusters=k, random_state=0).fit(colors)
            score = silhouette_score(colors, kmeans.labels_, sample_size=1000)
            silhouette_scores.append(score)

        return silhouette_scores.index(max(silhouette_scores)) + 2

    def group_colors(self, colors: np.array) -> np.array:
        best_k = self._find_optimal_k(colors)
        print("best_k: ", best_k)
        kmeans = KMeans(n_clusters=best_k, random_state=0).fit(colors)
        centers = np.array(kmeans.cluster_centers_.astype("uint8"))
        return centers


class EuclideanDistColorGroupingStrategy(ColorGroupingStrategy):
    def _group_colors(self, colors: np.array) -> np.array:
        if len(colors) > 0:
            # distances = cdist(colors[0:1], colors, metric=deltaE_distance_calculator.pairwise_deltaE_distance)[0]
            distances = np.array(list(np.linalg.norm(colors[0] - color) for color in colors))
            group = colors[distances <= 135]
            rest = colors[distances > 135]
            return [group] + self._group_colors(rest)
        return []

    def group_colors(self, colors: np.array) -> np.array:
        grouped_colors = self._group_colors(colors)
        print("group_count: ", len(grouped_colors))
        return [np.mean(group, axis=0) for group in grouped_colors]

