import cv2


def convert_to_jpg(image_file_path):
    new_image_path = ".".join(image_file_path.split(".")[:-1]) + ".jpg"
    image = cv2.imread(image_file_path)
    cv2.imwrite(new_image_path, image)


convert_to_jpg("../TestFiles/png_image.png")

