from setuptools import setup, find_packages

setup(
    name='Pokemon_AMG',
    version='1.0.0',
    author="Alexis",
    author_email="axelgoma11@gamil.com",
    description="Esta libreria contiene la facilidad de generar un pokemon aleatorio como una pokebola",
    packages=find_packages(),
    package_data={"Pokemon_AMG":["pokemon.csv"]},
    install_requires=[
        "pandas"
    ]
)