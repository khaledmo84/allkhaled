from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="alkhaled-ultimate",
    version="1.0.0",
    author="Khaled Mo84",
    author_email="khaledmo84@example.com",
    description="Decentralized autonomous trading bot for crypto markets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/khaledmo84/allkhaled",
    packages=find_packages(include=["alkhaled", "alkhaled.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.12.0",
            "flake8>=7.0.0",
            "mypy>=1.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "alkhaled=run:main",
        ],
    },
)
