from setuptools import setup, find_packages
import toml
import re

# Read the pyproject.toml file
with open('pyproject.toml') as f:
    data = toml.load(f)

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

author = data['tool']['poetry']['authors'][0]

# Extract email using regex
match = re.match(r'(.*) <(.*)>', author)
if match:
    author_name, author_email = match.groups()
else:
    author_name = author
    author_email = ''

name = data['tool']['poetry']['name']
dependencies = [
    "python>=3.8.1",
    "numpy>=1.24.1",
    "docutil==0.18.1",
    "sphinx-rtd-theme>=1.2.0",
    "toml>=0.10.2",
    "types-toml>=0.10.8.5"
]
version = data['tool']['poetry']['version']
description = data['tool']['poetry']['description']
repository = data['tool']['poetry']['repository']
license = data['tool']['poetry']['license']

setup(
    name=name,
    version=version,
    packages=find_packages(),
    install_requires=dependencies,
    author=author_name, 
    author_email=author_email,
    description=description,
    url=repository,
    license=license,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
