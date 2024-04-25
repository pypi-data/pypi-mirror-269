from setuptools import setup,find_packages

setup(
        name = "FMAPOKE",
        version = "1.0.0",
        author = "Fernando Martinez",
        author_email = "202224199_MARTINEZ@tesch.edu.mx ", 
        description = "Libreria para generar un Pokemón Aleatorio.",
        packages = ["FMAPOKE"],
        package_data = {'FMAPOKE': ["pokemon.cvs"]},
        install_requires = [
               'pandas'
        
        ]
        
        

)