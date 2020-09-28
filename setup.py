import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bamboo",
    version="0.1",
    author="rahul-acr",
    author_email="rahul.saha.c@gmail.com",
    description="Bamboo backup tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    scripts=['bin/bamboo'],
    url="https://github.com/rahul-acr/bamboo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
