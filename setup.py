import shutil
import os
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    content = f.readlines()
    requirements = [x.strip() for x in content]

root_path = os.path.split(os.path.abspath(__file__))[0]
db_path = os.path.join(root_path, 'db')


def get_file(path, all_files=[]):
    files = os.listdir(path)
    for file in files:
        f_path = os.path.join(path, file)
        if not os.path.isdir(f_path):   # not a dir
            all_files.append((path.replace(db_path, 'db'), [
                             f_path.replace(db_path, 'db')]))
        else:  # is a dir
            get_file(f_path, all_files)
    return all_files


data_files = get_file(db_path)

shutil.copyfile("start.py", 'cmder')

setup(
    name='cmder',
    version='1.0',
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
    data_files=data_files,
    # packages=find_packages(),
    scripts=['cmder'],
    packages=find_packages('src'),
    package_dir={'': "src"},
)

os.remove('cmder')
