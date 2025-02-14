from setuptools import setup, find_packages

setup(
    name="pupsis.py",
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
    description="Unofficial Python API wrapper for PUPSIS",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yam-1111/pupsis.py",
    license="HL3 License",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Hippocratic License 3.0 (HL3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)