import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
# This call to setup() does all the work
setup(
    name="msgraph-email",
    version="2.0.0",
    description="Automate your emails using Microsoft Graph API",    
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/pixelbyaj/msgraph-email",
    author="Abhishek Joshi - PixelbyAJ",
    author_email="pixelbyaj.dev@gmail.com",
    license="Apache",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.13",
    ],
    keywords="microsoft graph email outlook api",
    project_urls={
        "Documentation": "https://github.com/pixelbyaj/msgraph-email#readme",
        "Source": "https://github.com/pixelbyaj/msgraph-email",
    },
    packages=find_packages(include=["msgraph_email*"], exclude=["demo"]),
    include_package_data=True,
    install_requires=["requests", "msgraph-sdk","azure-identity"]
)