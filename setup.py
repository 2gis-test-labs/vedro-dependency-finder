from setuptools import find_packages, setup


def find_required():
    with open("requirements.txt") as f:
        return f.read().splitlines()


def find_dev_required():
    with open("requirements-dev.txt") as f:
        return f.read().splitlines()


setup(
    name="vedro-dependency-finder",
    version="1.0.0",
    description="Plugin helps to find dependencies of unstable tests by shuffling selected tests",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="2GIS Test Labs",
    author_email="test-labs@2gis.ru",
    python_requires=">=3.8",
    url="https://github.com/2gis-test-labs/vedro-dependency-finder",
    packages=find_packages(exclude=("tests",)),
    package_data={"vedro_dependency_finder": ["py.typed"]},
    install_requires=find_required(),
    tests_require=find_dev_required(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
    ],
)