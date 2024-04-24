from setuptools import setup, find_packages

setup(
    name='CVAT_Video_Annotation_Processor',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python',  # Add OpenCV as a dependency
        'xmltodict',  # Add xmltodict for XML parsing
    ],
)
