import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import math
from random import choice
from PIL import Image
from colorblind import colorblind
from SourceCode import pdf_generator
from SourceCode.detection_algs import array_to_img
from SourceCode.report_result_object import ReportResultObject


# Following method adapted from: https://github.com/ddecatur/VizExtract/blob/main/create_graph.py
def genData(data_type: str):
    """
    Generates data for type of chart specified in data_type
    :param data_type: Type of chart to generate data for
    :return: X1: series of points for coordinate 1, X2: series of points for coordinate 2
    """
    if data_type == 'line':
        # slope and intercept
        sign = [-1, 1]
        m = choice(sign) * np.random.random()  # determine slope
        b = choice(sign) * np.random.randint(0, 25) * np.random.random()  # determine intercept
        delta = np.random.uniform(-50, 50, size=(100,))
        X1 = np.arange(100)
        X2 = (m * X1) + b + delta
    elif data_type == 'bar':
        # slope and intercept
        sign = [-1, 1]
        m = choice(sign) * np.random.random()  # determine slope
        # b = choice(sign) * randint(0,50) * random() # determine intercept
        delta = np.random.uniform(-15, 15, size=(30,))
        X1 = np.arange(30)
        X2 = (m * X1) + delta

        # adjust intercept to make bar graph not cross y axis
        minVal = min(X2)
        # print(minVal)
        b = 0 - minVal
        X2 = (m * X1) + b + delta
    elif data_type == 'scatter':
        sign = [-1, 1]
        correlation = choice(sign) * np.random.random()
        Y1 = np.random.randn(1000)
        Y2 = np.random.randn(1000)
        phi = (0.5) * math.asin(correlation)
        a = math.cos(phi)
        b = math.sin(phi)
        c = math.sin(phi)
        d = math.cos(phi)
        X1 = (a * Y1) + (b * Y2)
        X2 = (c * Y1) + (d * Y2)

    return X1, X2


def generate_graph_images(target_dir: str) -> None:
    """
    Generates synthetic graph images
    :param target_dir: Target directory name to save the generated images to
    """
    os.makedirs(target_dir, exist_ok=True)
    colors = ['red', 'forestgreen', 'deepskyblue', 'yellow', 'darkorange']
    graph_types = ['scatter', 'line', 'bar']
    color_nums = [1, 2, 3]
    for ii in range(80):
        color_num = random.choice(color_nums)
        graph_type = random.choice(graph_types)
        color_choices = random.sample(colors, k=color_num)
        for i in range(0, color_num):
            x, y = genData(graph_type)
            if graph_type == 'scatter':
                plt.scatter(x, y, color=color_choices[i])
            elif graph_type == 'line':
                plt.plot(x, y, color=color_choices[i])
            elif graph_type == 'bar':
                width = 0.3
                plt.bar(x + np.random.uniform(-width, width), y, width, color=color_choices[i])

        plt.xlabel('X1')
        plt.ylabel('X2')
        plt.title(f"graph_{graph_type}_{color_num}_{ii}")
        img_name = f"{target_dir}/graph_prot_{graph_type}_{color_num}_{ii}.jpg"

        plt.savefig(img_name)
        plt.close()


def generate_dataset(dataset_name: str, image_source_dir: str) -> None:
    """
    Creates dataset from images in given directory
    :param dataset_name: Target dataset name
    :param image_source_dir: Directory of images name to create the dataset from
    """
    dataset = pd.DataFrame(columns=['image_filename', 'graph_type', 'color_count', 'triggers'])
    for filename in os.listdir(f"{image_source_dir}/"):
        image_info = filename.split("_")
        dataset = dataset.append({'graph_type': image_info[2], 'color_count': image_info[3],
                                  'image_filename': f"{image_source_dir}/{filename}", 'triggers': []
                                  }, ignore_index=True)
    dataset.to_csv(dataset_name, sep='\t', index=False)


def simulate_colorblindness(source_dir: str) -> None:
    """
    Simulates all types of colorblindness for images in the directory and saves them in pdf report file
    :param source_dir: Name of directory of images to simulate colorblindness for
    """
    i = 0
    for filename in os.listdir(f"{source_dir}/"):
        graph = Image.open(f"{source_dir}/{filename}")
        img = np.array(graph)
        prot_obj = ReportResultObject("Protanopia")
        deut_obj = ReportResultObject("Deuteranopia")
        trit_obj = ReportResultObject("Tritanopia")
        prot_obj.found, prot_obj.simulated = True, array_to_img(
            colorblind.simulate_colorblindness(img, colorblind_type='protanopia'))
        deut_obj.found, deut_obj.simulated = True, array_to_img(
            colorblind.simulate_colorblindness(img, colorblind_type='deuteranopia'))
        trit_obj.found, trit_obj.simulated = True, array_to_img(
            colorblind.simulate_colorblindness(img, colorblind_type='tritanopia'))
        pdf_generator.generate(os.path.join(os.getcwd(), 'Simulated', f'{i}.pdf'), filename,
                               f"{source_dir}/{filename}", [prot_obj, deut_obj, trit_obj])
        i += 1


# generate_graph_images('GroupingDataset')
# generate_dataset('no_grouping_dataset.csv', 'GroupingDataset')
simulate_colorblindness('GroupingDataset')
