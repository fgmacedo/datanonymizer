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
    install_requires=[
        'h3>=3,<4',
        'mimesis>=4,<5',
        'PyYAML>=5,<6',
    ],
    zip_safe=False,
    keywords='data anonymizer',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries',
        'Topic :: Security',
    ],
)
