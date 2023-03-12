import setuptools
from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    """
    This function will return list of requirements
    """
    requirement_list:List[str] = []

    """
    Write a code to read requirements.txt file and append each requirements in requirement_list variable.
    """
    return requirement_list

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "0.0.1" 

REPO_NAME = "Fake-News-Detecting-Training-Pipeline"
AUTHOR_USER_NAME = "vaasu2002"
SRC_REPO = REPO_NAME
AUTHOR_EMAIL = "vaasu.bisht2021@vitbhopal.ac.in"

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="Re-training pipeline that will be trigger when it gets latest fake news data.",
    long_description=long_description,
    long_description_content="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    install_requires=get_requirements(),
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    packages = find_packages()
)