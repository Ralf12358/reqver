from setuptools import setup, find_packages

setup(
    name='reqver',
    version='0.1.1',
    author='Your Name',
    author_email='your.email@example.com',
    description='A tool to add version information to requirements.txt files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/reqver',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click>=8.0.1',
        'pip>=21.1.3',
    ],
    entry_points={
        'console_scripts': [
            'reqver=reqver.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='requirements version pip',
    python_requires='>=3.6',
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/reqver/issues',
        'Source': 'https://github.com/yourusername/reqver/',
    },
)
