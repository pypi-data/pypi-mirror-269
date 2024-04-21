from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tire-code-parser",
    version="0.9.1",
    description="A package to parse tire codes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Stefior",
    author_email="contact@stefior.com",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
)

