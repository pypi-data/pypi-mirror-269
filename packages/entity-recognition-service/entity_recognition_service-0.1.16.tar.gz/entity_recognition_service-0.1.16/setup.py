from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="entity-recognition-service",
    version="0.1.16",
    author="Cesar Goncalves",
    author_email="goncalves.cesaraugusto94@gmail.com",
    description="A library for technology entity recognition and recommendation",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cgoncalves94/entity-recognition",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "bertopic==0.16.1",
        "spacy>=3.0.0",
        "transformers>=4.0.0",
        "torch>=1.0.0",
        "scikit-learn>=1.0.0",
        "scipy>=1.0.0",
        "pandas>=1.0.0",
        "aiofiles>=0.8.0",
    ],
)