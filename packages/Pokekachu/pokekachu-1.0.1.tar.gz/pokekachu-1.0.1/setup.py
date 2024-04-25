from setuptools import setup,find_packages

setup(
   name="Pokekachu",
   version = "1.0.1",
   author= "Maria Martinez",
   author_email= "202224015_martinez@tesch.edu.mx",
   description= "Librerias paran generar un Pokemon aleatorio",
   packages= ["Pokekachu"],
   package_data= {'Pokekachu': ["pokemon.csv"]},
   install_requires=[
   'pandas'
   ]
)