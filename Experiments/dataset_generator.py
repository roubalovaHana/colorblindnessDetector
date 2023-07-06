import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from random import choice
import math
import matplotlib.colors as mcolors


def genData(data_type):
    # determine variables
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
        delta = np.random.uniform(-15, 15, size=(50,))
        X1 = np.arange(50)
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


def generate_grouping_dataset():
    # Create the dataset
    dataset = pd.DataFrame(columns=['image_filename', 'graph_type', 'color_count', 'colors'])

    os.makedirs('GroupingDataset', exist_ok=True)
    colors = ['red', 'forestgreen', 'deepskyblue', 'yellow', 'darkorange']
    graph_types = ['scatter', 'line', 'bar']
    color_nums = [2, 3, 4, 5]
    for ii in range(50):
        color_num = random.choice(color_nums)
        graph_type = random.choice(graph_types)
        color_choices = random.sample([item for item in list(mcolors.CSS4_COLORS) if item not in colors], k=color_num-2)
        color_choices.extend(random.sample(colors, k=2))
        for i in range(0, color_num):
            x, y = genData(graph_type)
            if graph_type == 'scatter':
                plt.scatter(x, y, color=color_choices[i])
            elif graph_type == 'line':
                plt.plot(x, y, color=color_choices[i])
            elif graph_type == 'bar':
                width = 0.5
                plt.bar(x + np.random.uniform(-width, width), y, width, color=color_choices[i])

        plt.xlabel('X1')
        plt.ylabel('X2')
        plt.title(f"graph_{graph_type}_{color_num}_{ii}")
        img_name = f"GroupingDataset/graph_prot_{graph_type}_{color_num}_{ii}.jpg"
        dataset = dataset.append({'graph_type': graph_type, 'color_count': color_num, 'image_filename': img_name,
                                  'colors': color_choices}, ignore_index=True)
        plt.savefig(img_name)
        plt.close()
    # Save dataset as CSV
    dataset.to_csv('grouping_dataset.csv', sep='\t', index=False)


generate_grouping_dataset()
# from scipy.spatial import distance
# colors = [(255,0,0),(0,255,0),(0,0,255),(0,255,255),(255,0,255),(255,255,0),(0,0,0),(255,255,255),(130,130,130)]
# distances = []
# for i in range(len(colors)):
#     dist = []
#     for j in range(i+1, len(colors)):
#         dist.append(distance.euclidean(colors[i], colors[j]))
#     distances.append(dist)
# for dist_row in distances:
#     print(dist_row)
