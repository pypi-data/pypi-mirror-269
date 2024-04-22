import io
from setuptools import setup, find_packages

with io.open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='html_invoice_sender',
    version='0.3',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'Jinja2',
    ],
)
