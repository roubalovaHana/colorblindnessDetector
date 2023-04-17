import image_format_converter
import kmeans
from PIL import Image


def find_issues(image_file_path):
    image_format_converter.convert_to_jpg(image_file_path)
    graph = Image.open(image_file_path)
    grouped_colors = kmeans.group_colors(graph)


find_issues("../TestFiles/unfriendly_colormap.jpg")
