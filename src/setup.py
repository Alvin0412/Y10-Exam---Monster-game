
"""just ignore this file"""
from setuptools import setup, find_packages

__version__ = "0.01"
__author__ = "Alvin.li"

setup(
    install_requires=[
        'numpy>=1.23.0'
    ],
    entry_points={
        'console_scripts': [
            'monster_game = MonsterGame.main:main'
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Win32 (MS Windows)",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ],
    name="Monster Game",
    version=__version__,
    author=__author__,
    author_email="Alvin.li@harrowhaikou.cn",
    description="A simple monster game.",

    url="https://github.com/Alvin0412/Y10-Exam-Monster-game",
    packages=find_packages()
)
