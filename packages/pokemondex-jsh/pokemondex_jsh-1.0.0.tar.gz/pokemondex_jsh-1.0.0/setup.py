from setuptools import setup, find_packages

setup(
    name='pokemondex_jsh',
    version='1.0.0',
    author="Jeronimo Hernandez",
    author_email="sanchezhernandezjeronimo@gmail.com",
    description="Libreria para generar un pokemon aleatorio.",
    packages=find_packages(),
    package_data={'pokemondex_jsh': ['pokemon.csv']},
    install_requires=[
                      'pandas'
                      ]
)