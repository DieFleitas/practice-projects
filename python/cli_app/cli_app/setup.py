from setuptools import setup, find_packages

setup(
    name="cli_app",
    versiopn="1.0.0",
    packages=find_packages(),
    entry_points={"console_scripts": ["cli_app=app:main"]},
)