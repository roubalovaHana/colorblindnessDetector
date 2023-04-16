import ImageFormatConverter
import cv2
import k_means_clustering


def find_issues(image_file_path):
    ImageFormatConverter.convert_to_jpg(image_file_path)
    graph = cv2.imread(image_file_path)
    clusters = KMeansCluster(graph)
