# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages

BASE_DIR = os.path.realpath(os.path.dirname(__file__))

def parse_requirements():
    reqs = []
    if os.path.isfile(os.path.join(BASE_DIR, "requirements.txt")):
        with open(os.path.join(BASE_DIR, "requirements.txt"), 'r') as fd:
            for line in fd.readlines():
                line = line.strip()
                if line:
                    reqs.append(line)
    return reqs

if __name__ == "__main__":
    setup(
        name="k0s",
        version="0.0.1",
        description="A sample Python project k0s",
        author="random",
        author_email="random@gmail.com",
        cmdclass={},
        packages=find_packages(include=["src"]),
        package_data={'': ['*.txt', '*.TXT', '*.JS', 'test/*']},
        install_requires=parse_requirements(),
        entry_points={'console_scripts': ['demo = src.sample.simple:main']},

        license="Copyright(c)2024-2034 test All Rights Reserved."
    )
