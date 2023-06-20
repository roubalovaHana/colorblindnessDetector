import os
import cv2


def convert_to_jpg(image_file_path):
    new_image_path = os.path.splitext(image_file_path)[0]+'.jpg'
    image = cv2.imread(image_file_path)
    print(new_image_path)
    if not os.path.exists(new_image_path):
        cv2.imwrite(new_image_path, image)


# convert_to_jpg("../TestFiles/png_image.png")
