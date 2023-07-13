import ast

import numpy as np
import pandas as pd
import time
from abc import ABC, abstractmethod
from PIL import Image
from sklearn.metrics import accuracy_score

from SourceCode.color_grouping_algs import KMeansColorGroupingStrategy, ColorGroupingStrategy, \
    EuclideanDistColorGroupingStrategy, DeltaEDistColorGroupingStrategy
from SourceCode.deltaE_distance_calculator import convert_to_Lab
from SourceCode.detection_algs import DeltaDistanceDetection


class Context(ABC):

    def __init__(self, strategy: ColorGroupingStrategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> ColorGroupingStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: ColorGroupingStrategy) -> None:
        self._strategy = strategy

    # The template method
    def evaluate(self, threshold, lab):
        df = pd.read_csv('grouping_dataset.csv', sep='\t', header=0)
        expected_values = []
        predicted_values_unique = []
        for index, row in df.iterrows():
            image_path, expected_value = self.get_img_info(row)
            expected_values.append(expected_value)
            graph = Image.open(image_path)
            img = np.array(graph)
            unique_colors, counts = np.unique(np.array(list(graph.convert('RGB').getdata())), axis=0,
                                              return_counts=True)
            indices = np.argsort(counts)[::-1]
            unique_colors = unique_colors[indices]

            if lab:
                lab_list = list(map(convert_to_Lab, unique_colors))
                unique_colors = np.array([[lab_color[0].lab_a, lab_color[0].lab_b, lab_color[0].lab_l] for lab_color in lab_list])

            grouped_colors_unique = self.strategy.group_colors(unique_colors, threshold)
            predict_value_unique = self.predict_value(grouped_colors_unique, img)
            predicted_values_unique.append(predict_value_unique)
        accuracy_unique = self.calculate_accuracy(expected_values, predicted_values_unique)
        return accuracy_unique, expected_values, predicted_values_unique

    @abstractmethod
    def get_img_info(self, row):
        pass

    @abstractmethod
    def detect_triggers(self, grouped_colors, img):
        pass

    @abstractmethod
    def predict_value(self, grouped_colors, img):
        pass

    @abstractmethod
    def calculate_accuracy(self, expected_values, predicted_values):
        pass


class ThresholdEvaluator(Context):
    def get_img_info(self, row):
        return row['image_filename'], row['color_count'] + 2    # extra group for background and legend

    def detect_triggers(self, grouped_colors, img):
        return None

    def predict_value(self, grouped_colors, img):
        return len(grouped_colors)

    def calculate_accuracy(self, expected_values, predicted_values):
        return accuracy_score(expected_values, predicted_values)


class PerformanceEvaluator(Context):

    def get_img_info(self, row):
        return row['image_filename'], ast.literal_eval(row['triggers'])

    def detect_triggers(self, grouped_colors, img):
        return DeltaDistanceDetection().detect(grouped_colors, True, True, True, img)

    def predict_value(self, grouped_colors, img):
        exp_tri = []
        report_result_list = DeltaDistanceDetection().detect(grouped_colors, True, True, True, img)
        for ii in range(len(report_result_list)):
            if report_result_list[ii].found:
                exp_tri.append(1)
            else:
                exp_tri.append(0)
        return exp_tri

    def calculate_accuracy(self, expected_values, predicted_values):
        return self.acc_score(expected_values, predicted_values)

    def acc_score(self, expected, predicted):
        total_predictions = len(expected)*3
        differences = np.array(expected) - np.array(predicted)
        correct_predictions = np.count_nonzero(differences == 0)

        return correct_predictions / total_predictions


def PerformThresholdExperiments(target_dataset_name):
    concrete_strategies = [[EuclideanDistColorGroupingStrategy(), 'Euclid', 150, 251, 10, False],
                           [DeltaEDistColorGroupingStrategy(), 'deltaE', 30, 41, 1, False],
                           [EuclideanDistColorGroupingStrategy(), 'EuclidLab', 54, 101, 5, True]]
    results = pd.DataFrame(columns=["algorithm", "Threshold", "Accuracy Unique", "Run Time",
                                    'Expected values', 'Predicted values'])
    i = 0
    for strategy in concrete_strategies:
        evaluator = PerformanceEvaluator(strategy[0])
        print(strategy[1])
        for threshold in range(strategy[2], strategy[3], strategy[4]):
            start_time = time.time()
            acc_uniq, exp_vals, pred_vals_uniq = evaluator.evaluate(threshold, strategy[5])
            end_time = time.time()
            run_time = end_time - start_time
            results.loc[i] = [strategy[1], threshold, acc_uniq, run_time, exp_vals, pred_vals_uniq]
            print(f'threshold: {threshold}, accuracy: {acc_uniq}, run time: {run_time}')
            i += 1
    results.to_csv(target_dataset_name, sep='\t', index=False)


def PerformPerformanceExperiments(target_dataset_name):
    concrete_strategies = [[EuclideanDistColorGroupingStrategy(), 'Euclid', 190, False],
                           [DeltaEDistColorGroupingStrategy(), 'deltaE', 30, False],
                           [EuclideanDistColorGroupingStrategy(), 'EuclidLab', 60, True]]
    # ,
    #                            [KMeansColorGroupingStrategy(), 'K-meansUnique', 0, False]
    results = pd.DataFrame(columns=["algorithm", "Running time", "Accuracy",
                                    "Expected values", "Predicted values"])
    i = 0
    for strategy in concrete_strategies:
        evaluator = PerformanceEvaluator(strategy[0])
        print(strategy[1])
        start_time = time.time()
        accuracy, exp_vals, pred_vals = evaluator.evaluate(strategy[2], strategy[3])
        end_time = time.time()
        run_time = end_time - start_time
        print(f'Accuracy: {accuracy}, Run_time: {run_time}')
        results.loc[i] = [strategy[1], run_time, accuracy, exp_vals, pred_vals]
        i += 1
    results.to_csv(target_dataset_name, sep='\t', index=False)


def threshold_range_experiments():
    evaluator = ThresholdEvaluator(DeltaEDistColorGroupingStrategy())
    df = pd.read_csv('grouping_dataset.csv', sep='\t', header=0)
    first_df = df.loc[0]
    print(first_df['image_filename'])
    graph = Image.open(first_df['image_filename'])
    colors = np.array(list(graph.convert('RGB').getdata()))
    # lab_list = list(map(convert_to_Lab, colors))
    # colors = np.array([[lab_color[0].lab_a, lab_color[0].lab_b, lab_color[0].lab_l] for lab_color in lab_list])
    unique_colors, counts = np.unique(colors, axis=0, return_counts=True)
    indices = np.argsort(counts)[::-1]
    unique_colors = unique_colors[indices]
    for threshold in range(25, 71):
        grouped_colors = evaluator.strategy.group_colors(unique_colors, threshold)
        print(f'threshold: {threshold}, {len(grouped_colors)}')


PerformThresholdExperiments('threshold_performance_results.csv')
# PerformPerformanceExperiments('performance_results.csv')

