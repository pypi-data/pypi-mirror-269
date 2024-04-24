from setuptools import setup, find_packages

setup(

    name='Pokelib',
    version="1.0.0",
    author="Rodrigo Gonzalez",
    author_email="202224040_gonzalez@tesch.edu.mx",
    description="Libreria para crear un pokemon aleatorio.",
    packages=find_packages(),
    package_data={'Pokelib': ["pokemon.csv"]},
    install_requires=["pandas"]

)