import ast
import numpy as np
import pandas as pd
import time
from abc import ABC, abstractmethod
from PIL import Image
from SourceCode import detection_algs
from SourceCode.color_grouping_algs import KMeansColorGroupingStrategy, ColorGroupingStrategy, \
    EuclideanDistColorGroupingStrategy, DeltaEDistColorGroupingStrategy
from SourceCode.deltaE_distance_calculator import convert_to_Lab


class Context(ABC):
    """
    Serves as the context for the ColorGroupingStrategy.
    Defines a template method 'evaluate' for color grouping evaluation.
    """

    def __init__(self, strategy: ColorGroupingStrategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> ColorGroupingStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: ColorGroupingStrategy) -> None:
        self._strategy = strategy

    def evaluate(self, threshold: int, lab: bool):
        """
        The template method for color grouping evaluation.
        Reads the dataset and evaluates the color grouping accuracy and performance.
        :param threshold: The threshold value for color grouping.
        :param lab: A flag indicating whether to use the Lab color space.
        :return: A tuple containing the accuracy, expected values, and predicted values of color grouping.
        """
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
            unique_colors = self.preprocess_colors(unique_colors, counts)

            if lab:
                lab_list = list(map(convert_to_Lab, unique_colors))
                unique_colors = np.array(
                    [[lab_color[0].lab_a, lab_color[0].lab_b, lab_color[0].lab_l] for lab_color in lab_list])

            grouped_colors_unique = self.strategy.group_colors(unique_colors, threshold)
            predict_value_unique = self.predict_value(grouped_colors_unique, img)
            predicted_values_unique.append(predict_value_unique)
        accuracy_unique = self.calculate_accuracy(expected_values, predicted_values_unique)
        return accuracy_unique, expected_values, predicted_values_unique

    def get_img_info(self, row):
        """
        Retrieves the image filename and its expected colorblindness triggers from the dataset.
        :param row: Row from dataset with image information
        :return: A tuple containing the image filename and its expected colorblindness triggers.
        """
        return row['image_filename'], ast.literal_eval(row['triggers'])

    def predict_value(self, grouped_colors, img):
        """
        Predicts colorblindness issues based on the grouped colors and image
        :param grouped_colors: The grouped color values
        :param img: The image array for colorblindness simulation
        :return: A list of 0 or 1 representing the predicted colorblindness issues for given image.
        """
        exp_tri = []
        report_result_list = detection_algs.detect_colorblindness_issues(grouped_colors, True, True, True, img)
        for ii in range(len(report_result_list)):
            if report_result_list[ii].found:
                exp_tri.append(1)
            else:
                exp_tri.append(0)
        return exp_tri

    def calculate_accuracy(self, expected_values, predicted_values):
        """
        Calculates the accuracy of colorblindness prediction based on expected and predicted values
        :param expected_values: The expected colorblindness triggers
        :param predicted_values: The predicted colorblindness triggers
        :return: The accuracy score of colorblindness prediction.
        """
        return self.acc_score(expected_values, predicted_values)

    def acc_score(self, expected, predicted):
        """
        Calculates the accuracy of colorblindness prediction based on expected and predicted values
        Treats triggers for single image as three predictions and considers partially correct predictions
        :param expected: The expected colorblindness triggers
        :param predicted: The predicted colorblindness triggers
        :return: The accuracy score of colorblindness prediction.
        """
        total_predictions = len(expected) * 3
        differences = np.array(expected) - np.array(predicted)
        correct_predictions = np.count_nonzero(differences == 0)

        return correct_predictions / total_predictions

    @abstractmethod
    def preprocess_colors(self, unique_colors, counts):
        """
        An abstract method to preprocess the colors for color grouping evaluation.
        :param unique_colors: The unique color values for evaluation.
        :param counts: The counts of each unique color value.
        :return: The preprocessed color values for color grouping evaluation
        """
        pass


class KMeansEvaluator(Context):
    def preprocess_colors(self, unique_colors, counts):
        """
        Skips preprocessing
        :param unique_colors: The unique color values for evaluation.
        :param counts: The counts of each unique color value.
        :return: Unchanged unique_colors
        """
        return unique_colors


class PerformanceEvaluator(Context):
    def preprocess_colors(self, unique_colors, counts):
        """
        Sorts unique colors by its occurrence count in descending order.
        :param unique_colors: The unique color values for evaluation.
        :param counts: The counts of each unique color value.
        :return: Sorted colors by occurrence in descending order
        """
        indices = np.argsort(counts)[::-1]
        return unique_colors[indices]


def PerformThresholdExperiments(target_dataset_name: str) -> None:
    """
    Performs the threshold experiments for Euclidean distance paired with RGB, Euclidean distance paired with Lab
    and deltaE distance algorithms
    :param target_dataset_name: Target dataset name to save the evaluation results to
    """
    concrete_strategies = [[EuclideanDistColorGroupingStrategy(), 'Euclid', 150, 251, 10, False],
                           [EuclideanDistColorGroupingStrategy(), 'EuclidLab', 55, 101, 5, True],
                           [DeltaEDistColorGroupingStrategy(), 'deltaE', 20, 41, 1, False]]
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


def PerformKMeansPerformanceExperiments(target_dataset_name: str) -> None:
    """
    Performs performance experiment for K-Means algorithm
    :param target_dataset_name: target_dataset_name: Target dataset name to save the evaluation results to
    """
    results = pd.DataFrame(columns=["algorithm", "Running time", "Accuracy",
                                    "Expected values", "Predicted values"])

    evaluator = KMeansEvaluator(KMeansColorGroupingStrategy())
    print('K-means')
    for i in range(10):
        start_time = time.time()
        accuracy, exp_vals, pred_vals = evaluator.evaluate(0, False)
        end_time = time.time()
        run_time = end_time - start_time
        print(f'Accuracy: {accuracy}, Run_time: {run_time}')
        results.loc[i] = ['K-means', run_time, accuracy, exp_vals, pred_vals]
    results.to_csv(target_dataset_name, sep='\t', index=False)


def threshold_range_experiments() -> None:
    """
    Performs threshold experiment for single image from dataset.
    Used to determine the threshold range for experiments.
    """
    evaluator = PerformanceEvaluator(DeltaEDistColorGroupingStrategy())
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


# PerformThresholdExperiments('threshold_performance_results.csv')
PerformKMeansPerformanceExperiments('performance_kmeans_results.csv')
