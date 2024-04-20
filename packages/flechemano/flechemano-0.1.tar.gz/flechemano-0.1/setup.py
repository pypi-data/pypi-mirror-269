from setuptools import setup, find_packages

setup(
    name='flechemano',
    version='0.1',
    description='A package developed for blacktea024 to integrate it with PyPI.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='flechemano',
    url='https://github.com/flechemano/flechemano',
    packages=find_packages(),
    install_requires=[
        'blacktea024',
    ],
    python_requires='>=3.6',
)

