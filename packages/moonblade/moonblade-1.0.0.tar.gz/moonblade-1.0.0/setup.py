import codecs
import os
import pathlib
from setuptools import setup

import moonblade


path = pathlib.Path(__file__).parent

long_description = (path / "README.md").read_text(encoding="utf-8")

setup(
    name = moonblade.__title__,
    version = moonblade.__version__,
    description = moonblade.__description__,
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = moonblade.__url__,
    author = moonblade.__author__,
    author_email = moonblade.__author_email__,
    license = "MIT",
    classifiers = [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages = ["moonblade"],
    install_requires = [
        "httpx", "psutil", "websockets"
    ],
)