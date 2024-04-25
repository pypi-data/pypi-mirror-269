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
  name='matrix_multiplication',
  version='0.0.1',
  description='A package to multiply two matrix of any dimensions',
  long_description=open('README.txt').read() + '\n\n' + open('ChangeLog.txt').read(),
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