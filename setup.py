from setuptools import find_packages, setup


setup(
    name='JWM',
    version='1.0',
    author='Tjaart de Vries',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Operating System :: OS Independent'
        'Topic :: Security :: Cryptography',
        'Topic :: Security'
    ]
)
