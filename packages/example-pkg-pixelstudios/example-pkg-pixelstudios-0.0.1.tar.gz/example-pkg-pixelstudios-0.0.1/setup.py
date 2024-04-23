import setuptools

with open("README.txt", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="example-pkg-pixelstudios",
    # Replace with your own username above
    version="0.0.1",
    author="Jnanashree",
    author_email="x23174528@student.ncirl.ie",
    description="To calculate the extra price when choosing the type of album",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    # if you have libraries that your module/package/library
    #you would include them in the install_requires argument
    install_requires=[''],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)