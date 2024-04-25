import sys
from setuptools import setup, find_packages

install_requires = [
    'annotated-types>=0.6.0',
    'configparser>=6.0.1',
    'dnspython>=2.6.1',
    'pydantic>=2.6.4',
    'pydantic-settings>=2.2.1',
    'pydantic_core>=2.16.3',
    'pymongo>=4.6.3',
    'python-dotenv>=1.0.1',
    'typing_extensions>=4.10.0'
]

DESCRIPTION = "A database migration tool for MongoDB"

def get_read_me():
    try:
        with open('README.md') as f:
            return f.read()
    except IOError:
        return DESCRIPTION

setup(
    name='mongo_m',
    version='1.0.5',
    description=DESCRIPTION,
    long_description=get_read_me(),
    long_description_content_type="text/markdown",
    author='Dankov Sergey',
    author_email='beyond31@mail.ru',
    license='GNU General Public License v3 (GPLv3)',
    url='https://github.com/BeyonD311/mongo-m',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    zip_safe=False,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)