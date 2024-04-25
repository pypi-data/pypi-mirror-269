from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name="alert_on_exception",
    version="0.1.5",
    package_dir={"": "src"},  # This line is added
    packages=find_packages(where="src"),  # And this line is modified
    install_requires=[],
    python_requires=">=3.6",
    description="A Python package to alert users about exceptions.",  # Short, concise description
    long_description=long_description,  # Detailed description
    long_description_content_type="text/markdown",  # Content type for long description, assuming it's in Markdown
)
