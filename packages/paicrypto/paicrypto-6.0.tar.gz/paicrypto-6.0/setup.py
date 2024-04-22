from setuptools import setup, find_packages

setup(
    name='paicrypto',
    version='6.0',
    description='A collection of algorithms',
    author='Adithya Pai B',
    author_email='paiadithya26@gmail.com',
    packages= find_packages(),
    install_requires=[
        'pycryptodome'
        # Add any dependencies your project requires
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)