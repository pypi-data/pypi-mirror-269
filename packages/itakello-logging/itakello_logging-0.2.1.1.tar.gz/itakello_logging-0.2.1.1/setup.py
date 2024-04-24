from setuptools import find_packages, setup

setup(
    name="itakello_logging",
    version="0.2.1.1",
    author="Itakello",
    author_email="maxste000@gmail.com",
    description="A custom logging library by Itakello",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Itakello/itakello_logging",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
