import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kteppris",
    version="0.0.1",
    author="Keno Teppris",
    description="A simple excel and csv to LaTeX converter with PyQT GUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kteppris/excel2latex",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

