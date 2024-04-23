from setuptools import setup, find_packages

readme = open("./readme.md").read()

setup(
    name="pyreportgen",
    version="0.1.16",
    description="A package for creating reports and other pdf documents.",
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)