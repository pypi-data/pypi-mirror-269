from setuptools import setup, find_packages

setup(
    name='Pokesi',
    version='1.0.1',
    author="Bryan Salazar",
    author_email="bryan.nayrb.1071@gmail.com",
    description="Esta libreria contiene la facilidad de generar un pokemon aleatorio como una pokebola",
    packages=["Pokesi"], ##Todo lo que suba en la libreria me hara un mapeo de todos los paquetes
    package_data={"Pokesi":["pokemon.csv"]},
    #Automaticamente te va a instalar pandas
    install_requires=[
        "pandas"
]
)