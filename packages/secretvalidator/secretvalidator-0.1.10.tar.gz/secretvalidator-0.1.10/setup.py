from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='secretvalidator',
    version='0.1.10',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.txt'],
    },
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'secretvalidator=secretvalidator.cli:validate',
        ],
    },
)
