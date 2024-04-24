from setuptools import setup, find_packages

setup(
    name="pokemon_haru",
    version="1.0.0",
    author_email="harumissa4@gail.com",
    description="Lybrari para generaar un pokemon aleatorio",
    packages=find_packages(),
    package_data={"pokemon_haru": ["pokemon.csv"]},
    install_requires=[
        'pandas'
    ]
)