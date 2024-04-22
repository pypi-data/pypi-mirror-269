from setuptools import setup, find_packages

setup(
name='courieruuid',
version='0.1.0',
packages=find_packages(),
description='A courier service UUID generator',
long_description=open('README.md').read(),
long_description_content_type='text/markdown',
author='Rohith Konan Ravi',
author_email='rohithkr612@gmail.com',
url='https://github.com/RohithKonanRavi/courieruuid.git',
classifiers=[
'Development Status :: 3 - Alpha',
'Intended Audience :: Developers',
'License :: OSI Approved :: MIT License',
'Programming Language :: Python :: 3',
'Programming Language :: Python :: 3.7',
'Programming Language :: Python :: 3.8',
'Programming Language :: Python :: 3.9',
'Programming Language :: Python :: 3.10',
],
python_requires='>=3.7',
)
