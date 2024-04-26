#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time:2024/3/27 17:02
# Author:Zhang HongTao
# @File:setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='common-tools-ai-bnq',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # 依赖项列表
        'structlog==23.1.0',
        'concurrent-log-handler==0.9.22',
        'nacos-sdk-python==0.1.12',
        'PyYAML==6.0.1',
        'cos-python-sdk-v5==1.9.28',
    ],
    # 其他元数据，如作者、描述等
    author='BNQ',
    description='Common tools of AI module for BNQ',
    long_description=long_description,
    long_description_content_type="text/markdown",  # 指明内容类型为markdown
)
