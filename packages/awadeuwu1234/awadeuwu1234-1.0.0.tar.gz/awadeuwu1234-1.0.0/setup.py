from setuptools import setup,find_packages

setup(
name="awadeuwu1234",
version="1.0.0",
author="Fredd Foxx",
author_email="202224031_castillo@tesch.edu.mx",
description="Librería para generar un Pokémon aleatorio",
packages=find_packages(),
package_data={'awadeuwu1234':["pokemon.csv"]},
install_requires=[
'pandas'
]
)