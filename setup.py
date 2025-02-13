from setuptools import setup, find_packages

setup(
    name="pupsis",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "httpx",
        "selectolax",
        "hishel",
        "psutil",
    ],
    entry_points={
        "console_scripts": [
            "pupsis=pupsis.cli:main",
        ],
    },
    author="yam-1111",
    description="unofficial python api wrapper for PUPSIS",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yam-1111/pupsis.py",
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
