from setuptools import setup, find_packages

setup(
    name='Pokebola',
    version='1.0.4',
    author='Rogelio Guzman',
    author_email='miniroyerguzman@gmail.com',
    description='Libreria para generar un Pokemon aleatorio',
    packages=['Pokebola'],
    package_data={'Pokebola': ['pokemon.csv']},
    install_requires=[
        'pandas'
    ]
)
