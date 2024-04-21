from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="lawcord",
    version="0.1.0",
    author="law",
    description="A simple Discord bot library made by law",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lawlol/lawcord",
    packages=find_packages(),
    install_requires=[
        "websockets>=10.4",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.2.1",
            "flake8>=6.0.0",
            "black>=23.3.0",
        ],
        "docs": [
            "sphinx>=5.3.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Framework :: AsyncIO",
    ],
    python_requires='>=3.7',
    entry_points={
        "console_scripts": [
            "lawcord=lawcord.cli:main",
        ],
    },
    keywords="discord bot library asyncio",
    license="MIT",
)