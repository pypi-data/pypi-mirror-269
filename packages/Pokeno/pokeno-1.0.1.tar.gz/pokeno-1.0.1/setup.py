from setuptools import setup,find_packages

setup(
   name="Pokeno",
   version = "1.0.1",
   author= "Rogelio Guzman",
   author_email= "miniroyerguzmam@gmail.com",
   description= "Librerias paran generar un Pokemon aleatorio",
   packages= ["Pokeno"],
   packages_data= {"Pokeno": ["pokemon.csv"]},
   install_requires=[
   'pandas'
   ]
)