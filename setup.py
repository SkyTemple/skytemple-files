# mypy: ignore-errors
__version__ = '1.4.0'
import os

from setuptools import setup, find_packages

# README read-in
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
# END README read-in


def get_resources(file_exts):
    directory = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'skytemple_files', '_resources')
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            if any(filename.endswith(file_ext) for file_ext in file_exts):
                paths.append(os.path.join('_resources', os.path.relpath(os.path.join('..', path, filename), directory)))
    return paths


setup(
    name='skytemple-files',
    version=__version__,
    packages=find_packages(),
    package_data={'skytemple_files':
                  get_resources(['.xml', '.asm', '.rst', 'LICENSE', '.txt', 'md', '.bin', '.png', '.yml', '.yaml']) +
                  ['graphics/chara_wan/Shadow.png', 'py.typed']},
    description='Python library to edit the ROM of Pokémon Mystery Dungeon Explorers of Sky (EU/US)',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/SkyTemple/skytemple-files/',
    install_requires=[
        'ndspy >= 3.0.0',
        'pyyaml >= 6.0.0',
        'range-typed-integers >= 1.0.0',
        'Pillow >= 6.1.0',
        'appdirs >= 1.4.0',
        'explorerscript >= 0.1.1',
        'skytemple-rust >= 1.3.7',
        'tilequant >= 0.4.0',
        'typing-extensions == 3.7.4.2; python_version<"3.7"',
        'pyobjc==8.5; sys_platform == "darwin"',
        'dungeon-eos==0.0.5'
    ],
    entry_points='''
        [console_scripts]
        skytemple_export_maps=skytemple_files.export_maps:main
    ''',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
