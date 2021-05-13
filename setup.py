import io
from setuptools import setup


with io.open('README.rst', encoding='utf-8') as readme_file:
    readme = readme_file.read()

long_description = readme

setup(
    name="datanonymizer",
    version="0.1",
    description="Anonymizer tool for datasets such CSV files",
    long_description=long_description,
    url="http://github.com/fgmacedo/datanonymizer",
    author="Fernando Macedo",
    author_email="fgmacedo@gmail.com",
    license="MIT",
    packages=["datanonymizer"],
    entry_points={
        'console_scripts': [
            'datanonymizer=datanonymizer:main',
        ],
    },
    zip_safe=False,
)
