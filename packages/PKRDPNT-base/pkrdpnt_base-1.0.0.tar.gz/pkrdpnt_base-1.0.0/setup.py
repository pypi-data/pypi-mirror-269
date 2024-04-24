from setuptools import setup, find_packages

setup(name='PKRDPNT-base',
      version='1.0.0',
      description='Una libreria que genera un pokemon aleatorio',
      author='Christopher Ruiz',
      author_email='202224135_ruiz@tesh.edu.mx',
      packages=find_packages(),
      package_data={'PKRDPNT': ["pokemon.csv"]},
      install_requires=['pandas']
      )
