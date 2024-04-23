from setuptools import setup, find_packages
from dgcloud.cli import __version__

setup(
    name='dgcloud',
    version=__version__,
    packages=find_packages(),
    author='Dhinagaran (Dg)',
    author_email='dhinagaran1411@gmail.com',
    url='https://github.com/Dhinagaran-s/dgcloud',
    include_package_data=True,
    install_requires=[
        'click',
        'pyyaml',
        'paramiko',
    ],
    entry_points={
        'console_scripts': [
            'dgcloud=dgcloud.cli:main',
        ],
    }
)
