from setuptools import setup, find_packages

# README read-in
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
# END README read-in

setup(
    name='skytemple-files',
    version='0.0.2a3',
    packages=find_packages(),
    package_data={'skytemple_files': ['_resources/**/*']},
    description='Python library to edit the ROM of Pokémon Mystery Dungeon Explorers of Sky (EU/US)',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/SkyTemple/skytemple-files/',
    install_requires=[
        'ndspy >= 3.0.0',
        'Pillow >= 6.1.0',
        'appdirs >= 1.4.0',
        'explorerscript >= 0.0.2a1',
        'typing-extensions == 3.7.4.2; python_version<"3.7"'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
)
