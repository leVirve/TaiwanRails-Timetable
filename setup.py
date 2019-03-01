from setuptools import setup, find_packages

setup(
    name='taiwan-rails',
    description='Taiwan Rails Timetable',
    url='https://github.com/leVirve/TaiwanRails-Timetable/',
    author='leVirve',
    version='0.3.0',
    license='GPL 2.0',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.6, <4',
    install_requires=[
        'requests',
        'click',
        'lxml',
    ],
    extras_require={
        'dev': ['pylint'],
        'test': ['coverage'],
    },
    entry_points={
        'console_scripts': [
            'train=timetable.cli:main',
        ],
    },
)
