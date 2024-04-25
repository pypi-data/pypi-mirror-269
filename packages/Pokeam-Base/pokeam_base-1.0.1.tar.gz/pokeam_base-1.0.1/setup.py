from setuptools import setup, find_packages

setup(
    name='Pokeam_Base',
    version='1.0.1',
    author='Father1',
    author_email='202224143_trejo@tesch.edu.mx',
    description='Libreria para generar un pokemon aleatorio',
    packages=["Pokeam_Base"],
    package_data={'Pokeam_Base': ['pokemon.csv']},
    install_requires=[
        "pandas"
    ],
)