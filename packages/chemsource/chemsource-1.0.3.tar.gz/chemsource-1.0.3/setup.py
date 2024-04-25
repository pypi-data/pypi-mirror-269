from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="chemsource",
    author="Prajit Rajkumar",
    author_email="prajkumar@ucsd.edu",
    description="Tool to classify novel drugs and other health-related" 
                + " chemicals by origin",
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "lxml>=4.9.4",
        "openai>=1.23.2",
        "requests>=2.0.0,<3",
        "wikipedia>=1.4.0",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)