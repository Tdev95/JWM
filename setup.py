from setuptools import find_packages, setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='JWM',
    version='1.0',
    author='Tjaart de Vries',
    author_email='t.de.vries.22@student.rug.nl',
    description='WIP',
    url='https://github.com/Tdev95/JWM',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Operating System :: OS Independent'
        'Topic :: Security :: Cryptography',
        'Topic :: Security'
    ],
    install_requires=['pymacaroons'],
    python_requires='>=3.6'
)
