from setuptools import setup, find_packages

import numpy as np

 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='matMulti',
  version='0.0.3',
  description='A package to multiply two matrix of any dimensions',
  long_description=open('README.txt').read(),
  long_description_content_type='text/plain',
  url='https://github.com/SajalDasShovon/Own-Simple-Python-Package',  
  author='Sajal Das Shovon',
  author_email='shovon030cse.kuet@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='matrixMultiplier', 
  packages=find_packages(),
  install_requires=[''] 
)