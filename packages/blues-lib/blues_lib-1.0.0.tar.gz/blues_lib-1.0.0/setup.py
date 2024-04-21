from setuptools import setup,find_packages

setup(
  name="blues_lib", # package name
  version="1.0.0", # package version
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  packages=find_packages(), # package module
  install_requires=[
    'Pillow>=10.3.0',
    'Requests>=2.31.0'
  ] # package dependency
)