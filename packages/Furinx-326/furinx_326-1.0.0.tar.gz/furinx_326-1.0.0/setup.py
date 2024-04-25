from setuptools import setup, find_packages
setup(
name= 'Furinx_326',
version='1.0.0',
author='LexZeik',
authoremail ='israellg0987@gmail.com',
description='Pokemon Aleatorio',
packages = find_packages(),
package_data={'FurinX_32': ['pokemon.csv']},
install_requires=['pandas'],
)
