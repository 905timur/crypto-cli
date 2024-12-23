from setuptools import setup, find_packages

setup(
    name="crypto-cli-tool",
    version="0.0.2",
    packages=find_packages(),  # Automatically include all the packages in your project
    install_requires=[
        "requests",  # Required for HTTP requests
        "fuzzywuzzy"  # Required for fuzzy string matching
    ],
    entry_points={
        "console_scripts": [
            "crypto.cli=crypto.cli.tool:main",  # Maps 'crypto.cli' to the main function in crypto.cli.tool
        ],
    },
    author="Timur Gabaidulin",
    description="A CLI tool to fetch cryptocurrency prices.",
    url="https://github.com/905timur/crypto-cli",  # GitHub repository URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Ensures compatibility with Python 3.6 or higher
)
