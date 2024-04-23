from setuptools import setup, find_packages, Extension
from sqlUts import version

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='sqlUts',
  version=version,
  description='An orm package',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type='text/markdown',
  url='',  
  author='Melque Lima',
  author_email='melque_ex@yahoo.com.br',
  license='MIT', 
  classifiers=classifiers,
  keywords='sqlUts', 
  packages=find_packages(),
  install_requires=['SQLAlchemy<2.0.0','SQLAlchemy-Utils'] 
  # install_requires=['SQLAlchemy==1.4.0','SQLAlchemy-Utils==0.38.2'] 
)
