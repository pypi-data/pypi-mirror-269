from setuptools import setup, find_packages
setup(
    name='poketnas',
    version='1.0.0',
    author="Christopher Reynoso",
    author_email="202224134_reynoso@tesch.edu.mx",
    description="Libreria para generar un pokemon aleatorio.",
    packages=find_packages(),
    package_data={'poketnas': ['pokemon.csv']},
    install_requires=(
        "pandas"
    )


)