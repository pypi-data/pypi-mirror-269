from setuptools import setup, find_packages

setup(
    name="pokeme",
    version="1.0.0",
    author="Farid Hernandez",
    author_email= "jaelfarid261@gmail.com",
    descripcion = "Libreria para generar un pokemon aleatorio.",
    package = find_packages(),
    package_data= {'pokeme': ["pokemon.csv"]},
    install_requires= [
    'pandas'
    ]
)