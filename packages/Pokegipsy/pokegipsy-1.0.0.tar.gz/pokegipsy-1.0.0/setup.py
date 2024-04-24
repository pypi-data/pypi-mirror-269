from setuptools import setup, find_packages

setup(
    name='Pokegipsy',
    version='1.0.0',
    author='Fernando Gonzalez',
    author_email='ferglezcc@gmail.com',
    description='Libreria para generar un pokemon aleatorio',
    packages=find_packages(),
    package_data={'Pokegipsy': ['pokemon.csv']},
    install_requires=[
        'pandas',
    ],
)