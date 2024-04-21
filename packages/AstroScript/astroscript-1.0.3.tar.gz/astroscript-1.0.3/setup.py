from setuptools import setup, find_packages
from astroscript.version import __version__

setup(
    name='AstroScript',  # Name of your project
    version=__version__,  # Version number
    author='Mikael Folkesson',  # Your name or your organization/company name
    author_email='mikael.folkesson@gmail.com',  # Your email address
    description='Astrological calculation tool',  # Short description of your project
    long_description=open('README.md').read(),  # Long description read from the README.md
    long_description_content_type="text/markdown",  # Type of the long description, here markdown
    url='https://github.com/Shoresh613/astro-script/',  # Link to your project's GitHub repo
    packages=find_packages(include=['astroscript', 'astroscript.*']),  # Automatically find and include all packages
    install_requires=[
        'pytz', 'pyswisseph', 'geopy', 'tabulate',  # List your project's dependencies
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',  # Development status of your project
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',  # License as approved by OSI
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.6',  # Minimum version requirement of the package
    keywords='astrology, horoscopes, charts',
    # scripts=['bin/astroscript'],  # Optional: Include any executable scripts you have
    include_package_data=True,  # Include all relevant files from your MANIFEST.in
    package_data={
        'astroscript': [
            'ephe/*',    # All files in the 'ephe' subdirectory
            'font/*',    # All files in the 'font' subdirectory
            '*.txt',     # All TXT files in the root of the package
            '*.webp'     # All WEBP files in the root of the package
        ]
    },
    # package_data={
    #     # Include any package data files
    #     'astroscript': ['data/*.dat']
    # },
    entry_points={
        'console_scripts': [
            'astroscript=astroscript.astroscript:main',  # CLI version in astroscript.py
            'astroscript_gui=astroscript.main:main'  # GUI version in main.py
        ],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/Shoresh613/astro_script/issues',
        'Source': 'https://github.com/Shoresh613/astro_script/',
    },
)
