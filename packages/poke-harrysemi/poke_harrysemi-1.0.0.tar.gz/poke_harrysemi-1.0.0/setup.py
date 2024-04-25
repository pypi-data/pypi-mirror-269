from setuptools import setup,find_packages
setup(
    name='poke-harrysemi',
    version='1.0.0',
    author='Semiramis Del Castillo',
    author_email="202224131_galicia@tesch.edu.mx",
    description="una biblioteca que contiene la clase llamada RandomPOkemonpara generar un pokemon aleatorio",
    packages=find_packages(),
    package_data={'poke-harrysemi': ['pokemon.csv']},
    install_requires=[
        'pandas',
    ],
)