from setuptools import setup, find_packages

setup(
    name='faultier',
    version='0.1.4',
    packages=find_packages(),
    package_data={
        'faultier': ['../docs/*.svg'],
        'faultier': ['../example_firmware/*.hex'],
    },
    install_requires=[
        'pyserial', 'plotly'
    ],
    author='Thomas \'stacksmashing\' Roth',
    author_email='code@stacksmashing.net',
    description='A library to control the Faultier glitcher.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        
        'Operating System :: OS Independent',
    ],
)
