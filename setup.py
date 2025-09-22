# Copyright (C) 2025 APH10
# SPDX-License-Identifier: Apache-2.0

from setuptools import setup, find_packages
from apiclient.version import VERSION

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read().split("\n")

setup_kwargs = dict(
    name='sbomlenscli',
    version=VERSION,
    description='SBOMLens Command Line Interface',
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/APH10/SbomLensAPI",
    author='APH10',
    author_email='support@aph10.com',
    maintainer='APH10 Developers',
    maintainer_email='support@aph10.com',
    license='Apache-2.0',
    keywords=["security", "tools", "SBOM", "DevSecOps", "SPDX", "CycloneDX"],
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    python_requires=">=3.9",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "sbomlenscli = apiclient.cli:main",
        ],
    },
)

setup(**setup_kwargs)
