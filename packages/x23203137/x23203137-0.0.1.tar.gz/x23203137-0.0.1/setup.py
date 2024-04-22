import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="x23203137",
    # Replace with your own username above
    version="0.0.1",
    author="arun",
    author_email="arunshaji209@gmail.com",
    description="Package for ridersclub",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/x23203137/riders_safety",
    packages=setuptools.find_packages(),
    install_requires=[''],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
