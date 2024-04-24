from setuptools import setup, find_packages

setup(
    name='poke_frm_donpolloloco',
    version='1.0.0',
    author= "FernandoRoldan",
    author_email="roldanf661@gmail.com",
    description="LIBRERIA QUE GENRA UN POKEMON DE DONPOLLOLO, ES DECIR UN POKEMON ALEATORIO",
    packages=find_packages(),
    package_data= {'poke_frm_donpolloloco': ['pokemon.csv']},
    install_requires = ['pandas'],
)