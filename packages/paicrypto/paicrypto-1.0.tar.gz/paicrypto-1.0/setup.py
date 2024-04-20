from setuptools import setup, find_packages

setup(
    name='paicrypto',
    version='1.0',
    description='A collection of algorithms',
    author='Adithya Pai B',
    author_email='paiadithya26@gmail.com',
    packages= find_packages(),
    install_requires=[
        'pycrypto',
        'pycryptodome',
        # Add any dependencies your project requires
    ],
)