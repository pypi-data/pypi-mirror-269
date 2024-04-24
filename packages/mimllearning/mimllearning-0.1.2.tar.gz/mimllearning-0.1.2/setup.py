from setuptools import setup, find_packages
setup(
name='mimllearning',
version='0.1.2',
author='Damián Martínez Ávila',
author_email='damianmartinezavila@gmail.com',
description='MIML Library',
packages=["src/miml", "src/miml/classifier", "src/miml/data","src/miml/datasets", "src/miml/test", "src/miml/transformation", "src/miml/tutorial"],
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)