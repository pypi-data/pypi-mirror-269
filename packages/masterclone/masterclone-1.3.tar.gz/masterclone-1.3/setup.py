from setuptools import setup, find_packages

setup(
    name="masterclone",
    version="1.3",
    author="caique9014",
    author_email="oldtimesonz@gmail.com",
    description="A tool for cloning Git repositories",
    url="https://github.com/NpmMaster/MasterClone.git",
    packages=find_packages(),
    install_requires=['setuptools','typer'],  # Add any dependencies here
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
