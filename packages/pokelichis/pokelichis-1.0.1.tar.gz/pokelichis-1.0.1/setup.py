from setuptools import setup,find_packages
setup(
    name='pokelichis',
    version="1.0.1",
    author='<LIZBETH DIAZ>',
    autor_email='202224032_cid@edu.mx',
    description='Una blibloteca que contiene la clase para generar un pokemon aleatorio',
    packages=['pokelichis'],
    package_data={'pokelichis': ['pokemon.csv']},
    install_requires=[
    "pandas",
    ],
)