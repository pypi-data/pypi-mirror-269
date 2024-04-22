import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RoboCupDBA_RAI",
    version="0.1",
    author="whaly",
    author_email="whalykj@gmail.com",
    description="A small example package MongoDB Robo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/whaly-w/robocup",
    packages=setuptools.find_packages(),
    install_requires=[
        'dnspython',
        'install',
        'pymongo'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)