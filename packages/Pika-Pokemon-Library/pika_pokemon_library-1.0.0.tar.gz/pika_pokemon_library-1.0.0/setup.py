from setuptools import  setup,find_packages

setup(
    name="Pika_Pokemon_Library",
    version="1.0.0",
    author="Fernanda ",
    author_email="fernandacolin777@gamil.com",
    description="Library para generar un  Pokemon aleatoria ",
    packages=find_packages(),
    package_data={'Pika_Pokemon_Library':["pokemon.csv"]},
    install_requires=[
        'pandas'
    ]
)