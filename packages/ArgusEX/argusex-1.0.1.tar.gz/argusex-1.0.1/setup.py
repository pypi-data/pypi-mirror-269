from setuptools import setup,find_packages

setup(
    name="ArgusEX",
    version="1.0.1",
    author="JMEX",
    author_email="kvkgif95949@gmail.com",
    description="Libreria para generar un pokemin aleatoriamento",
    packages=find_packages(),
    package_data={"ArgusEX": ["Poc.csv"]},
    install_requires=[
        "pandas"
    ]
)