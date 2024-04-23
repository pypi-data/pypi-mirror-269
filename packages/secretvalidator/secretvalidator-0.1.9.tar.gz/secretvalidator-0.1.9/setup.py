from setuptools import setup, find_packages

setup(
    name='secretvalidator',
    version='0.1.9',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'secretvalidator=secretvalidator.cli:validate',
        ],
    },
)
