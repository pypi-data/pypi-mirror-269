from setuptools import setup, find_packages

setup(
    name='GS-Edit', 
    version='0.2.0',
    description='The Best Code Editor - GS',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  
    author='James Kaddissi',
    author_email='jameskaddissi@gmail.com',
    url='https://github.com/james-kaddissi/yourproject',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'PyQt5',  
        'QScintilla',
        'jedi'
    ],
    entry_points={
        'console_scripts': [
            'gs=gsedit.cli:run', 
        ],
    },
    python_requires='>=3.6',
)
