from setuptools import setup, find_packages

setup(
    name="converttentotwenty",
    version="3.0.1",
    description="Ma bibliothèque Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Joris-ROBIN/Converttentotwenty.git",
    author="Skairipa",
    author_email="jorisrobin34@gmail.com",
    license="MEEF",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=[
    ]
)
