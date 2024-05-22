from setuptools import setup, find_packages

setup(
    name="string_similarity",
    version="1.0.0",
    author="Ebrahim Shami",
    author_email="qsomeis@gmail.com",
    description="A library for calculating distance/similarity of two strings using various algorithms.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/qfewzz/string-similarity",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(where="."),
    python_requires=">=3.10",
    install_requires=[
        "py_stringmatching>=0.4.5",
    ],
)

