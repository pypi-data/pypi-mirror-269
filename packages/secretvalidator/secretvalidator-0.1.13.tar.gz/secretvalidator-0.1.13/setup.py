from setuptools import setup, find_packages
import os

# Get the path to requirements.txt which is one folder up
requirements_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.', 'requirements.txt'))

# Read requirements from requirements.txt
with open(requirements_path, 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='secretvalidator',
    version='0.1.13',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.txt', '../requirements.txt'],
    },
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'secretvalidator=secretvalidator.cli:validate',
        ],
    },
)
