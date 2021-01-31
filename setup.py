import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pypbbot",
    version="0.1a1",
    author="Kale1d0",
    author_email="kale1d0@qq.com",
    description="Python implementation for ProtobufBot Server.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PHIKN1GHT/pypbbot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)