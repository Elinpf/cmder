import shutil
import os
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    content = f.readlines()
    requirements = [x.strip() for x in content]

shutil.copyfile("cmder.py", 'cmder')

setup(
    name='cmder',
    version='0.1',
    author='Elin',
    description='Simple CLI tool for the generation hack commands.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Elinpf/cmder',
    classifiers=[
        'Environment :: Console'
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Security',
    ],
    python_requires='>=3.6',
    install_requires=requirements,
    packages=find_packages('cmder'),
    package_data={
        "": ["*.xd"]
    },
    scripts=['shellerator']
)

os.remove('cmder')
