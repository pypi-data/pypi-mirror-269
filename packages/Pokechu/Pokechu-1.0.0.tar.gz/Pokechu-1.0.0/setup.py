from setuptools import setup, find_packages

setup(
	name="Pokechu",
	version="1.0.0",
	author="Andrew Morales", 
	author_email="202224047_morales@tesch.edu.mx",
	description="Libreria para generar pokemon aleatorio",
	packages=find_packages(),
	package_data={'Pokechu': ["pokemon.csv"]},
	install_requires=[
		'pandas'
	]
	
)