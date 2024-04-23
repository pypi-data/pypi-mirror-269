from setuptools import setup, find_packages

setup(
    name='senfenico',
    version='0.1.1',

    description="Python bindings for the Stripe API",
    long_description="Python bindings for the Stripe API",
    long_description_content_type="text/x-rst",
    author="Senfenico",
    author_email="contact@senfenico.com",
    url="https://github.com/senfenico/senfenico-python",
    license="MIT",
    keywords="Senfenenico api payments",


    packages=find_packages(),
    install_requires=[
        'requests', 
    ]
)