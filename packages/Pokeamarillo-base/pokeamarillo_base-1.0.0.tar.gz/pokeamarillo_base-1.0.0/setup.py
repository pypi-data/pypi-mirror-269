from setuptools import setup, find_packages

setup(
name ="Pokeamarillo_base",
version ="1.0.0",
author="Brian Flores",

author_email = "20224036_flores@tesch.edu.mx", 
description = "libreria para generar un pokemon aleatorio",
 packages = find_packages(),
 package_data={'Pokeamarillo-base':["pokemon.cvs"]},
 install_requires=["pandas"]
)