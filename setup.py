import pathlib
from setuptools import setup,find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
# This call to setup() does all the work
setup(
    name="msgraph-email",
    version="1.0.0",
    description="Read/Send emails using Microsoft Graph API",    
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/realpython/reader",
    author="PixelByAJ - Abhishek Joshi",
    author_email="pixelbyaj@gmail.com",
    license="MIT",
    py_modules=["email\msgraph\__init__.py","email\msgraph\models\__init__.py"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("demo")),
    include_package_data=True,
    install_requires=["requests", "msgraph-core","azure-identity"],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)