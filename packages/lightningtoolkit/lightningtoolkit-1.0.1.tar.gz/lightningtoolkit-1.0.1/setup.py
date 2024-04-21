from setuptools import setup,find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    description = fh.read()
setup(
    name = "lightningtoolkit",
    version = "1.0.1",
    author = "GQX",
    author_email = "kill114514251@outlook.com",
    packages = find_packages(),
    description = "A toolkit that combines many functions",
    long_description = description,
    url = "https://github.com/BinaryGuo/Lightning_Toolkit",
    classifiers = [
        "Intended Audience :: End Users/Desktop",
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3"
    ],
    python_requires=">=3.0"
)