#!/usr/bin/env python
import io
import setuptools

with open('requirements.txt', encoding="utf-8") as f:
    requirements = f.read()

setuptools.setup(
    # Metadata
    name='testcase_10',
    version='0.0.1',
    author='Huading Su',
    author_email='shd_596@163.com',
    description='testcase_10',
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    python_requires='>=3.10',
    license='Attribution-NonCommercial-ShareAlike 4.0',
    # Package info
    install_requires=requirements
)