import os
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    content = f.readlines()
    requirements = [x.strip() for x in content]

root_path = os.path.split(os.path.abspath(__file__))[0]

setup(
    name='cmder_elinpf',
    version='2.2.2',
    author='Elin',
    description='Simple CLI tool for the generation hack commands.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Elinpf/cmder',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Security',
    ],
    python_requires='>=3.6',
    install_requires=requirements,
    # packages=find_packages(),
    scripts=['bin/cmder'],
    packages=find_packages('src'),
    package_dir={'': "src"},
)
