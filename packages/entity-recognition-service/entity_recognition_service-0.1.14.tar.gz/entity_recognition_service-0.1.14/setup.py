from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import sys

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)  # Run the standard install process
        try:
            # Attempt to download the spaCy model
            subprocess.check_call([sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'])
        except subprocess.CalledProcessError:
            print("Failed to install the spaCy model 'en_core_web_sm'. Please install it manually by running:")
            print("'python -m spacy download en_core_web_sm'")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="entity-recognition-service",
    keywords="entity recognition, recommendation, technology",
    license="MIT",
    version="0.1.14",
    author="Cesar Goncalves",
    author_email="goncalves.cesaraugusto94@gmail.com",
    description="A library for technology entity recognition and recommendation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cgoncalves94/entity-recognition",
    packages=find_packages(where=".", exclude=["tests", "tests.*"]),
    package_data={
        "entity_recognition_service": [
            "data/*",
            "functions/*",
        ],
    },
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
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio>=0.15.1",
            "async-asgi-testclient>=1.4.1",
        ],
    },
    cmdclass={
        'install': PostInstallCommand,  # Use the post-install command class defined above
    },
)