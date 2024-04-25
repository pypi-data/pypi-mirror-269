from setuptools import setup, find_packages

setup(
    name='PokebolaMari',
    version='1.0.3',
    author="Maria Cortes",
    author_email="maris235@outlook.com",
    description="Esta libreria contiene la facilidad de generar un pokemon aleatorio como una pokebola",
    packages=find_packages(),
    package_data={'PokebolaMari':["pokemon.csv"]},
    install_requires=[
        'pandas'
]
)