from setuptools import setup, find_packages

setup(
    name='essential_packages',
    version='0.3',
    packages= find_packages(),
    install_requires =[

    ],

    entry_points ={
        "console_scripts":[
            
            "codex = essential_packages:hello",
        ],
    },
)