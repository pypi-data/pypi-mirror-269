from setuptools import setup, find_packages

setup(
    name='essential_packages',
    version='0.4',
    packages= find_packages(),
    install_requires =[

    ],
    entry_points={
        "console_scripts": [
            
            "codex-hello = essential_packages:hello",
        ],
    },
)