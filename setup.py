from setuptools import setup, find_packages
from os import path
working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='scrapeddit', # name of packe which will be package dir below project
    version='0.2.0',
    url='https://github.com/Mafaz03/ReditScraper',
    author='Mafaz03',
    author_email='mohdmafaz200303@gmail.com',
    description='Simple test package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['praw', 'torchinfo'],
)