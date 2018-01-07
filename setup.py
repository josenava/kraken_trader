from setuptools import setup, find_packages

setup(
    name='kraken_trader',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
