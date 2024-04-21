
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="log_ex_simple",
    version="0.1",
    author="Yadots",
    author_email="stoday@gmail.com",
    description="A simple logging function to log messages to the screen or to a file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stoday/log_ex",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)

