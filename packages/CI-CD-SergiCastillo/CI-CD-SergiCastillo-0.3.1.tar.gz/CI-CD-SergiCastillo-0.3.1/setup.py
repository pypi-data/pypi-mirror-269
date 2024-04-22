import os
from setuptools import setup, find_packages

# Obtener la versión actual del paquete
version = '0.3.1'

# Eliminar el archivo .tar.gz existente si ya está presente
if os.path.exists(f"dist/CI-CD-SergiCastillo-{version}.tar.gz"):
    os.remove(f"dist/CI-CD-SergiCastillo-{version}.tar.gz")

setup(
    name='CI-CD-SergiCastillo',
    version=version,
    packages=find_packages(),
    install_requires=[
        'coverage',
        'pylint',
        'pytest',
        'ggshield',
        'psycopg2',
        'flask',
        'json-log-formatter',
        'twine'
    ],
    author='Sergi Castillo',
    description='KeepCoding',
    url='https://github.com/sergicastin/CI-CD-SergiCastillo',
)
