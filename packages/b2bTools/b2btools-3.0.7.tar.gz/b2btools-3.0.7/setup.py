#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools
import os

from b2bTools_version.versioning import PYPI_VERSION

current_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.dirname(current_dir)
docker_dir = os.path.join(root_dir, 'docker')
path_to_file = os.path.join(current_dir, "README.md")

dependencies = {
    "python_version == '3.7'": os.path.join(current_dir, 'requirements-py37.txt'),
    "python_version == '3.8'": os.path.join(current_dir, 'requirements-py38.txt'),
    "python_version == '3.9'": os.path.join(current_dir, 'requirements-py39.txt'),
    "python_version == '3.10'": os.path.join(current_dir, 'requirements-py310.txt'),
    "python_version == '3.11'": os.path.join(current_dir, 'requirements-py311.txt'),
    "python_version == '3.12'": os.path.join(current_dir, 'requirements-py312.txt'),
}

with open(path_to_file, "r") as f:
    long_description = f.read()

dependencies_to_install = []
for constraint, requirements_file in dependencies.items():
    with open(requirements_file, "r") as f:
        dependencies = f.readlines()
    for dependency in [d.rstrip() for d in dependencies if not d.startswith("#")]:
        dependencies_to_install.append(f"{dependency};{constraint}")

print(dependencies_to_install)

setuptools.setup(
    name="b2bTools",
    version=PYPI_VERSION,
    author="Wim Vranken",
    author_email="Wim.Vranken@vub.be",
    description="bio2Byte software suite to predict protein biophysical properties from their amino-acid sequences",
    license="OSI Approved :: GNU General Public License v3 (GPLv3)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    maintainer="Jose Gavalda-Garcia, Adrian Diaz, Wim Vranken",
    maintainer_email="jose.gavalda.garcia@vub.be, adrian.diaz@vub.be, wim.vranken@vub.be",
    url="https://bio2byte.be",
    project_urls={
        "Documentation": "https://bio2byte.be/b2btools/package-documentation",
        "HTML interface" : "https://bio2byte.be/b2btools"
    },
    packages=setuptools.find_packages(exclude=("**/test/**",)),
    include_package_data=True,
    keywords="bio2byte,b2bTools,biology,bioinformatics,bio-informatics,fasta,proteins,protein-folding",
    classifiers=[
        "Natural Language :: English",
        # Python 3.7 Release date: 2018-06-27, End of full support: 2020-06-27
        "Programming Language :: Python :: 3.7",
        # Python 3.8 Release date: 2019-10-14, End of full support: 2021-05-03
        "Programming Language :: Python :: 3.8",
        # Python 3.9 Release date: 2020-10-05, End of full support: 2022-05-17
        "Programming Language :: Python :: 3.9",
        # Python 3.10 Release date: 2021-10-04, End of full support: 2023-04-05
        "Programming Language :: Python :: 3.10",
        # Python 3.11 Release date: 2022-10-24, End of full support: 2024-04-01
        "Programming Language :: Python :: 3.11",
        # Python 3.12 Release date: 2023-10-02, End of full support: 2025-05
        "Programming Language :: Python :: 3.12",
        # License
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        # OS
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        # Topics
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
        # Audience
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        # Development Status
        "Development Status :: 5 - Production/Stable"
    ],
    python_requires=">=3.7, <3.13",
    install_requires=dependencies_to_install,
    entry_points={
        "console_scripts": [
            "b2bTools = b2bTools.__main__:main",
        ],
    },
)
