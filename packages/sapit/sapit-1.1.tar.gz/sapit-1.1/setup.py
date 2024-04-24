from setuptools import setup, find_packages

setup(
    name = 'sapit',
    version = '1.1',
    packages = find_packages(),
    install_requires = [
        'pyttsx3 == 2.90' 
    ],

    entry_points = {
        "console_scripts": [
            "sapit = sapit:say",
        ],
    },
)