from setuptools import setup, find_packages

setup(
    name='html_invoice_sender',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'Jinja2',
    ],
)
