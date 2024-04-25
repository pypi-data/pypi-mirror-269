from setuptools import setup, find_packages

setup(
    name='PokeCorky',
    version='1.0.1',
    author= "Victor Diaz",
    author_email="20222_diaz@tesch.edu.mx",
    description="Una biblioteca que contiene la clase RandomPokemon para generar un pokemon aleatorio",
    packages=[
        "PokeCorky",
    ],
    package_data={'PokeCorky': ['pokemon.csv']},
    install_requires=[
        "pandas",
    ],
)