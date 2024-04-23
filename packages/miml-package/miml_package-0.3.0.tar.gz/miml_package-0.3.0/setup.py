from setuptools import setup, find_packages
setup(
name='miml-package',
version='0.3.0',
author='Damián Martínez Ávila',
author_email='damianmartinezavila@gmail.com',
description='MIML Library',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)