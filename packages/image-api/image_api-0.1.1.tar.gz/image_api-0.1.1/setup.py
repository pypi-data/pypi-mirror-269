import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
    
setuptools.setup(
    name="image-api",
    version="0.1.1",
    description="A local and lightweight image search API",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="lkaijie",
    author_email="",
    url="https://github.com/lkaijie/image-api",
    packages=setuptools.find_packages(),
    install_requires=["requests", "beautifulsoup4"],
    keywords=["api", "myanimelist", "bing image", "google image", "images", "google"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)