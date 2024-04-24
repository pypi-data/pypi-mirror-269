from setuptools import setup, find_packages

setup(
    name='daac',
    version='0.1',
    author='Your Name',
    author_email='your.email@example.com',
    description='A package to echo contents of programs.py to clipboard',
    packages=find_packages(),
    install_requires=[
        'pyperclip'
    ],
    entry_points={
        'console_scripts': [
            'daac = daac.programs:main'
        ]
    }
)
