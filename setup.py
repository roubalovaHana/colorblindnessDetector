from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='colorblind_detector',
    version='0.1.0',
    packages=find_packages(),
    install_requires=install_requires,
    url='',
    license='',
    python_requires='==3.7',
    author='Hana Roubalová',
    author_email='',
    description='An application with a graphical interface that determines if a graph image is colorblind-friendly or not. '
)
