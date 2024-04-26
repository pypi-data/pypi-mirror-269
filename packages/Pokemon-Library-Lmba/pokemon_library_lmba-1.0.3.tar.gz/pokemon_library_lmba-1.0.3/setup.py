from setuptools import setup, find_packages
setup(
    name="Pokemon_Library-Lmba",
    version="1.0.3",
    author="Litzy Barrera",
    author_email="202224128_barrera@tesch.edu.mx",
    description="Libreria para generar un pokemon aleatorio.",
    packages=["Pokemon_Library-Lmba"],
    package_data={"Pokemon_Library-Lmba": ["pokemon.csv"]},
    install_requires= [
        "pandas",
    ],
)