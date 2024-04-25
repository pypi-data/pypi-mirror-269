from setuptools import setup,find_packages

setup(
    name="PokeapiMHM",
    version="1.0.0",
    author="Martha Morales",
    author_email="martha_mh@tesch.edu.mx",
    description="Librería para generar un Pokemón aleatoria.",
    packages=find_packages(),
    package_data={'Pokeapi': ["pokemon.csv"]},
    install_requires=[
        'pandas'
    ]
)
