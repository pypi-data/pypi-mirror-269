from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mysql_server_has_gone",
    version="2.0.3",
    description="Django myslq backend that fixes issue with long living connection",
    author="maiyajj",
    author_email="1045373828@qq.com",
    license="MIT",
    url="https://github.com/maiyajj/MySQL-server-has-gone-away",
    long_description=long_description,
    packages=find_packages(),
    long_description_content_type="text/markdown",
)
