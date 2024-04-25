from setuptools import  setup,find_packages

setup(
    name="Pika_Pokemon_Library",
    version="1.0.1",
    author="Fernanda ",
    author_email="fernandacolin777@gamil.com",
    description="Library para generar un  Pokemon aleatoria ",
    packages=["Pika_Pokemon_Library"],
    package_data={'Pika_Pokemon_Library':["pokemon.csv"]},
    install_requires=[
        'pandas'
    ]
)
