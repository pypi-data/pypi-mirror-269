from setuptools import setup, find_packages

setup(
    name="pokecuilmas",
    version="1.0.0",
    author="Daniel Rayon",
    author_email="202224029_beltran@tesch.edu.mx",
    description="Libreria para generar un pokemon aleatorio",
    packages=find_packages(),
    package_data={"pokecuilmas":["pokemon.csv"]},
    install_requires=[
        "pandas"
    ]
)
