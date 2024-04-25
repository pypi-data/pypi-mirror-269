from setuptools import setup,find_packages

setup(
   name="Pokekachu",
   version = "1.0.0",
   author= "Maria Martinez",
   author_email= "quinaprinces@gmail.com",
   description= "Librerias paran generar un Pokemon aleatorio",
   packages= find_packages(),
   package_data= {'Pokekachu': ["pokemon.csv"]},
   install_requires=[
   'pandas'
   ]
)