from setuptools import setup, find_packages

setup(
    name="Pokemon_Library_ENattRL",
    version="1.0.0",
    author="Natt",
    author_email="202224050_ramos@tesch.edu.mx",
    description="Libreria para buscar un pokemon aleatorio",
    packages=find_packages(),
    package_data={"Pokemon_Library_ENattRL":["pokemon.csv"]},
    install_requires=[
            "pandas"
       ]
)