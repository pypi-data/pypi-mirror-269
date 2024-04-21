from setuptools import setup, find_packages
with open('README.md') as f:
    long_description = f.read()

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: MacOS',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3.8'
]
 
setup(
  name='hima-discount',
  version='0.0.2',
  description='This is simple Discount calculator',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='',  
  author='Hima Shree ',
  author_email='X23189851@student.ncirl.ie',
  license='MIT', 
  classifiers=classifiers,
  keywords='Discount , Discount calculator', 
  packages=find_packages(),
  install_requires=[''] 
)