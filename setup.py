#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إعداد وتثبيت نظام إدارة المتجر
"""

from setuptools import setup, find_packages
import os

# قراءة README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# قراءة المتطلبات
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="store-management-system",
    version="1.0.0",
    author="علي - Ali",
    author_email="ali@example.com",
    description="نظام شامل لإدارة المتاجر والمؤسسات التجارية باللغة العربية",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ali/store-management-system",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Office/Business",
        "Topic :: Office/Business :: Financial",
        "Natural Language :: Arabic",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "store-management=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.qss", "*.md", "*.txt"],
    },
    keywords="store management arabic business finance debt installment internet",
    project_urls={
        "Bug Reports": "https://github.com/ali/store-management-system/issues",
        "Source": "https://github.com/ali/store-management-system",
        "Documentation": "https://github.com/ali/store-management-system/wiki",
    },
)
