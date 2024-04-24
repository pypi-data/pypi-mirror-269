from setuptools import setup, find_packages
setup(
    name="Pokemon_Library-Lmba",
    version="1.0.0",
    author="Litzy Barrera",
    author_email="202224128_barrera@tesch.edu.mx",
    description="Libreria para generar un pokemon aleatorio.",
    packages=find_packages(),
    package_data={"Pokemon_Library_Lmba": ["pokemon.csv"]},
    install_requires= [
        "pandas"
    ]
)