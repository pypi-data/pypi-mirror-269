from setuptools import setup, find_packages

setup(name='PKRDPNT',
      version='1.0.2',
      description='Una libreria que genera un pokemon aleatorio',
      author='Christopher Ruiz',
      author_email='202224135_ruiz@tesh.edu.mx',
      packages=["PKRDPNT"],
      package_data={'PKRDPNT': ["pokemon.csv"]},
      install_requires=['pandas']
      )
