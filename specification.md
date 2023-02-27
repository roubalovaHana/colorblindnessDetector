# Automatic Color-Blindness Detection in Data Visualizations
## Objective:
This project aims to create an application with a graphical interface that will determine if a graph image is colorblind-friendly or not. The program will analyze the colors of a given image and check if they are distinguishable for people with different types of color blindness.

## Functional Requirements:
- The application will have a graphical interface allowing the user to select an image from a computer (? or provide the URL address of an image?).
- The application will then perform the **k-means** algorithm on the preprocessed image to find the color groups in the graph.
- The application will then map these grouped colors to the corresponding colors in different types of color blindness (protanopia, deuteranopia, or tritanopia) using the **Colorblind** library.
- The application will then compute the **deltaE distances**.
- The application will issue a warning if some deltaE distances are too small, therefore indistinguishable by the human eye (? <3?).
- The application will display the warning in the graphical interface.

## Non-Functional Requirements:
- The program shall be developed using **Python** using the **PyCharm** development environment.
- The program shall use **PyQt5** for the graphical interface.
- The program shall use **OpenCV** for image processing.
- The program shall use **Matplotlib** for visualizing images.
- The program shall use **Pandas** for generating reports.
- The program shall be compatible with **Windows** operating system.
- The program shall have a responsive and user-friendly **graphical interface**.
- The program shall be easy to install and use.

## Program structure:
The program structure will consist of three parts. The first part will be the user interface module that will display the warnings and handle the design and the image selection.

The second part will be the business logic that will manage the preprocessing and analysis of the provided image.

The third part will be implementing a Facade design pattern that will encapsulate the program logic and simplify the communication between the design handling logic and the business logic.

## Assumptions:
- The input image is in a standard PNG, JPEG, or BMP format.
- The input image is not excessively large or complex.
