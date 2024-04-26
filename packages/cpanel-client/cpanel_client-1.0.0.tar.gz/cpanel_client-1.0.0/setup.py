import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "cpanel-client",
    version = "1.0.0",
    author = "nafiz",
    author_email = "sminrana@gmail.com",
    description = "A Python package for interacting with WHM + cPanel",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/smnafiz/python-cpanel-api",
    project_urls = {
        "Bug Tracker": "https://github.com/smnafiz/python-cpanel-api/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)