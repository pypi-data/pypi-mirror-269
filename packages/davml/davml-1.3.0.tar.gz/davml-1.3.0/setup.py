from setuptools import setup, find_packages

setup(
    name='davml',
    version='1.3.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A package to echo contents of programs.py to clipboard',
    packages=find_packages(),
    install_requires=[
        'pyperclip',
        'markdown2',
        'google.generativeai'
    ],
    entry_points={
        'console_scripts': [
            'dav = davml.programs:main',
            'ml = davml.program:main',
            'chat = davml.chat:chat'
        ]
    }
)






