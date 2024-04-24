from setuptools import setup, find_packages

setup(
    name='Pokeam',
    version='1.0.0',
    author='Father1',
    author_email='202224143_trejo@tesch.edu.mx',
    description='Libreria para generar un pokemon aleatorio',
    packages=find_packages(),
    package_data= {'Pokeam': ['pokemon.csv']},
    install_requires=[
        "pandas"
    ]
)