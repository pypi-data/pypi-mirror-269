from setuptools import setup, find_packages

setup(
    name='Pokesi',
    version='1.0.0',
    author="Bryan Salazar",
    author_email="bryan.nayb.1071@gmail.com.com",
    description="Esta libreria contiene la facilidad de generar un pokemon aleatorio como una pokebola",
    packages=find_packages(), ##Todo lo que suba en la libreria me hafa un mapeo de todos los paquetes
    package_data={"pokebolaMari":["pokemon.csv"]},
    #Automaticamente te va a instalar pandas
    install_requires=[
        "pandas"
]
)