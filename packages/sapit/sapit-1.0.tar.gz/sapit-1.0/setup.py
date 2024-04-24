from setuptools import setup, find_packages

setup(
    name = 'sapit',
    version = '1.0',
    packages = find_packages(),
    install_requires = [
        'pyttsx3 == 2.90' 
    ],
)