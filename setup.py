from setuptools import setup, find_packages

setup(
    name='reqver',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'reqver=reqver.cli:main',
        ],
    },
)
from setuptools import setup, find_packages

setup(
    name='reqver',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click==8.0.1',
        'pip==21.1.3',
    ],
    entry_points={
        'console_scripts': [
            'reqver=reqver:main',
        ],
    },
)
