# setup.py
from setuptools import setup, find_packages

def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content

setup(
    name='auto_batch_pull',
    version='0.1.0',
    description=
    'Automatically batch execute `git pull` command on all primary folders under the specified directory to update the repository to the latest version',
    author='Guofeng Yi',
    author_email='mark.yi@foxmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'abp=auto_batch_pull.main:main',
        ],
    },
    install_requires=[
        # '依赖包'
    ],
    python_requires='>=3.6',
    license='Apache License 2.0',
    long_description=readme(),
    long_description_content_type='text/markdown',
)
