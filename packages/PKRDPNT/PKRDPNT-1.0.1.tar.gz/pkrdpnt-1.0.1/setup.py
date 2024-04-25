from setuptools import setup, find_packages

setup(name='PKRDPNT',
      version='1.0.1',
      description='Una libreria que genera un pokemon aleatorio',
      author='Christopher Ruiz',
      author_email='202224135_ruiz@tesh.edu.mx',
      packages=find_packages(),
      package=["PKRDPNT"],
      package_data={'PKRDPNT-base': ["pokemon.csv"]},
      install_requires=['pandas']
      )
