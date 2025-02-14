from setuptools import setup, find_packages

setup(
    name="cathay_test_project",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "pytest",
        "webdriver-manager"
    ],
)