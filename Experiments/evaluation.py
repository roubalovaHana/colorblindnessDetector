import numpy as np
import pandas as pd
from PIL import Image
from sklearn.metrics import accuracy_score, confusion_matrix

from SourceCode.color_grouping_algs import KMeansColorGroupingStrategy, ColorGroupingStrategy, \
    EuclideanDistColorGroupingStrategy, DeltaEDistColorGroupingStrategy


class Context:

    def __init__(self, strategy: ColorGroupingStrategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> ColorGroupingStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: ColorGroupingStrategy) -> None:
        self._strategy = strategy

    def evaluate(self):
        results = pd.DataFrame(columns=["threshold", "Accuracy"])
        df = pd.read_csv('grouping_dataset.csv', sep='\t', header=0)
        i = 0
        for threshold in range(100, 260, 10):
            expected_values = []
            predicted_values = []
            for index, row in df.iterrows():
                image_path = row['image_filename']
                expected_values.append(row['color_count'] + 1)  # extra group for background
                # preparing image
                graph = Image.open(image_path)
                colors = np.array(list(set(graph.convert('RGB').getdata())))   # all colors
                # calling grouping strategy
                grouped_colors = self.strategy.group_colors(colors, threshold)
                # print(grouped_colors)
                predicted_values.append(len(grouped_colors))
            accuracy = accuracy_score(expected_values, predicted_values)
            results.loc[i] = [threshold, accuracy]
            i += 1
        results.to_csv(f'euclidean_uc_threshold_results.csv', sep='\t', index=False)


# concrete_strategies = [EuclideanDistColorGroupingStrategy()]# , KMeansColorGroupingStrategy(), DeltaEDistColorGroupingStrategy()]
context = Context(EuclideanDistColorGroupingStrategy())
context.evaluate()
# for i in range(0, len(concrete_strategies)):
#     context.strategy = concrete_strategies[i]
#     context.evaluate()
