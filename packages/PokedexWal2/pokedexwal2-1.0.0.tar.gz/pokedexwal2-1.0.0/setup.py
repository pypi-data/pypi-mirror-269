from setuptools import setup,find_packages
setup(
    name="PokedexWal2",
    version="1.0.0",
    author="El Wal2",
    author_email="202224042_marin@tesch.edu.mx",
    description="Libreria para generar un Pokémon aleatorio\n de la generacion 1 a la generacion 6",
    packages=find_packages(),
    package_data={'PokedexWal2': ['pokemon.csv']},
    install_requires=[
        'pandas'
    ]
)