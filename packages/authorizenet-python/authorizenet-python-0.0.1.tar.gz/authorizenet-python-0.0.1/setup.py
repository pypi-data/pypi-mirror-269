from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "A simple interface to the Authorize.Net APIs"

setup(
    name="authorizenet-python",
    version=VERSION,
    author="Jake Williamson",
    author_email="<brianjw88@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        "requests",
        "pydantic",
    ],
    keywords=["python", "authorize.net", "authorize"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
)
