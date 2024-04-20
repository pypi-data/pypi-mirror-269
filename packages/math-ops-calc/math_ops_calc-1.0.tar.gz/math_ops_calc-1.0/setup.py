from setuptools import setup, find_packages

setup(
    name='math_ops_calc',
    version='1.0',
    author='hem',
    author_email='hemanthmada001@gmail.com',
    description='A Python package for basic mathematical operations',
    long_description='''This package provides functions for performing basic mathematical operations such as addition, subtraction, multiplication, division, and modulo.''',
    long_description_content_type='text/markdown',
    url='https://github.com/Hemanth-Mada/math_operations',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
