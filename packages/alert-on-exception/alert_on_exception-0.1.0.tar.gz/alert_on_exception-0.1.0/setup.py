from setuptools import setup, find_packages

setup(
    name="alert_on_exception",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # add any additional packages needed
        "python-dotenv",
    ],
    python_requires=">=3.6",
)
