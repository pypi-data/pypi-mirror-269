from setuptools import setup,find_packages

setup(
          name="ViscaBarca",
          version="1.0.0",
          author="Angel Flores ",
          author_gmail= "af361488@gmail.com",
          description= "Libreria para generar un pokemon aleatorio",
          packages=find_packages(),
          package_data={"ViscaBarca": ["pokemon.csv"]},
          install_requires=[
          "pandas" 
          ]
          
          )