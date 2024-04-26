import setuptools

with open("README.md", "r", encoding='utf-8') as file:
    long_description = file.read()

setuptools.setup(
    name="grigode-env-2",
    version="1.0",
    author="Angel Chávez",
    author_email="infoangelchavez@gmail.com",
    description="grigode-env-2 is a library for reading and managing key-value pairs from .env files in your projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/angelchavez19/grigode-env-2",
    project_urls={
        "Bug Tracker": "https://github.com/angelchavez19/grigode-env-2/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    packages=setuptools.find_packages(),
    python_required=">=3.10"
)
