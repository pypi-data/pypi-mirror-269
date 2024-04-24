from setuptools import setup, find_packages

setup(
    name='mmpbsa-analysis-software',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'mdtraj',
        'tkinter'
    ],
    entry_points={
        'console_scripts': [
            'mmpbsa-analysis = main:run_mmpbsa_analysis'
        ]
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='MMPBSA Analysis Software using GROMACS and APBS',
    license='MIT',
    keywords='mmpbsa gromacs apbs charmm amber',
    url='https://github.com/yourusername/mmpbsa-analysis-software'
)
