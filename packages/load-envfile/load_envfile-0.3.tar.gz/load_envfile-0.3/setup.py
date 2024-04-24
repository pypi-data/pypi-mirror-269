from setuptools import setup, find_packages

setup(
    name='load_envfile',
    version='0.3',
    packages=find_packages(),
    description='Una biblioteca para cargar variables de entorno desde un archivo',
    author='María Muñoz Cruzado',
    author_email='maria.munozcruzado@telefonica.com',
    install_requires=[
        'python-dotenv',
    ],
)