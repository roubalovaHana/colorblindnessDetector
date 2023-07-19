# Automatic Color-Blindness Detection in Data Visualizations
This application was developed as the implementation part of my Bachelors Thesis
for the Computer Science program with Artificial Intelligence specialization
at Charles University.

## Objective
The Colorblind Detector application aims to help users determine 
if a graph image is colorblind-friendly. It analyzes the colors 
in the image and checks if they are distinguishable for people with 
different types of color blindness.

## System Requirements:
- Windows Operating System
- Python version 3.7
- Required Python packages: 
  - setuptools~=65.3.0
  - Kivy~=2.1.0
  - kivymd~=1.1.1
  - numpy~=1.20.2
  - Pillow~=9.2.0
  - Jinja2~=3.1.2
  - xhtml2pdf~=0.2.11
  - colorblind~=0.0.9
  - scipy~=1.7.3
  - scikit-learn~=1.0.2
  - colormath~=3.0.0
  - pandas~=1.3.5
  - matplotlib~=3.5.3
  - opencv-python~=4.6.0.66

## Installation
Follow these steps to set up the application:
1. Download the zip Colorblindness Detector project from https://github.com/roubalovaHana/colorblindnessDetector
2. Extract the project to a desired location on the computer.
3. Open the project in IDE and create a 3.7 Python interpreter.
4. Install the required Python packages by running the following command in the terminal:

                          pip install -r requirements.txt
5. Once the installation is complete, launch the application.

## Application interface
The Colorblind Detector application provides a user-friendly graphical interface. 
After launching the application, the main screen will appear with five buttons for 
controlling the application and three checkboxes for selecting the color vision deficiency

## Usage
### Loading image
Press the Load button and find the desired image in the file manager. Selecting a folder
of images is also possible by pressing the check button while in the file manager. In this 
case, the first image in the selected folder will display.
### Navigating folder
To navigate the images, use the Prev and Next buttons. The Prev button will display the 
previous image in the folder, while the Next button will display the following image.
### Choosing the type of color vision deficiency for analysis
The checked boxes indicate the selected types of color vision deficiencies for analysis.
Choose the desired combination by selecting appropriate checkboxes.
### Starting analysis
Pressing the Check button will start the analysis, which may take a while. After the 
analysis, if the image is unfriendly, a warning will display next to the corresponding 
color vision deficiency. If no warnings appear, the picture is colorblind friendly.
### Downloading the analysis report
After the analysis, download the pdf report about the current image by pressing the 
Download button. The report will show the original image and a simulated image for each 
triggered deficiency. Therefore, if no issues were triggered, no report will download.
## Limitations
The application assumes that the input image is in a standard PNG or JPEG format. It is not excessively large or complex. And that the image is of a single graph.
The application has no memory. When loading the same image, the analysis must be performed again.