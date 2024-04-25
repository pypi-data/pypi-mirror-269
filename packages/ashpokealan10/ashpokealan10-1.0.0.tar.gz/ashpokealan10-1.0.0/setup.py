from setuptools import setup, find_packages

setup(
    name='ashpokealan10',
    version='1.0.0',
    author="ASH",
    author_email="202224114_sanchez@tesch.edu.mx",
    description="Libreria para generar un pokemon aleatorio",
    packages=find_packages(),
    package_data={'ashpokealan10': ['pokemon.csv']},
    install_requires=[
        'pandas'
    ]

)