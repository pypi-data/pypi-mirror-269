from setuptools import setup,find_packages

setup(
name="Pokelmgr",
version="1.0.0",
author="Luz Gonzalez",
author_email="202224155_gonzalez@tesch.edu.mx",
description="Libreria para generar un Pokemon aleatoro.",
packages=find_packages(),
package_data={'Pokelmgr': ["pokemon.csv"]},
install_requires=[
'pandas'
]


)
