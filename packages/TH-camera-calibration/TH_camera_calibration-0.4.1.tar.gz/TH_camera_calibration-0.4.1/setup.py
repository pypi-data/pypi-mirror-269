from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="TH_camera_calibration",
    version="0.4.1",
    packages=find_packages(),
    install_requires=[
        "numpy==1.26.4",
        "opencv_contrib_python==4.8.1.78",
        "opencv_python==4.9.0.80",
        "PyYAML==6.0.1",
    ],
    long_description=description,
    long_description_content_type="text/markdown",
)
