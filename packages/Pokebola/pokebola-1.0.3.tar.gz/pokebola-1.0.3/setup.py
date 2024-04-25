from setuptools import setup, find_packages

setup(
    name='Pokebola',
    version='1.0.3',
    author='Rogelio Guzman',
    author_email='miniroyerguzman@gmail.com',
    description='Libreria para generar un Pokemon aleatorio',
    packages=find_packages(),
    package_data={'Pokebola': ['pokemon.csv']},
    install_requires=[
        'pandas'
    ]
)
