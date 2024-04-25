from distutils.core import setup
from setuptools import setup, find_packages
import json
from pathlib import Path
from typing import Optional

setup(
    name = "SAMBA_ilum",
    version = "1.0.0.3",
    entry_points={'console_scripts': ['samba_ilum = samba_ilum:main']},
    description = "...",
    author = "Augusto de Lelis Araujo", 
    author_email = "augusto-lelis@outlook.com",
    license = "Closed source",
    install_requires=['numpy',
                      'requests',
                      'pyfiglet',
                      'vasprocar'],
    package_data={"": ['*.dat', '*.png', '*.jpg', '*']},
)


# python3 -m pip install --upgrade twine
# python setup.py sdist
# python -m twine upload dist/*