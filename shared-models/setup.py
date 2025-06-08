from setuptools import setup, find_packages

setup(
    name="shared-models",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Django>=4.2",
        "djangorestframework>=3.14",
    ],
)