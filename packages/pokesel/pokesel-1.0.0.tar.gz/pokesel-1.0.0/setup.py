from setuptools import setup,find_packages
setup(
    name='pokesel',
    version='1.0.0',
    author="Selene Garcia",
    author_email="202224041_hernandez@tesch.edu.mx",
    description="Una bibliotec que tiene la clase  RandomPokemon para generar un pokemon aleatorio",
    packages=find_packages(),
    packages_data={'pokesel':['pokemon.csv']},
    install_requires=[
        "pandas",
    ],
)
