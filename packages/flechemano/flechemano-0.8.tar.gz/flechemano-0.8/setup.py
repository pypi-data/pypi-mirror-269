from setuptools import setup, find_packages

setup(
    name='flechemano',
    version='0.8',
    description='A package developed for blacktea024 to integrate it with PyPI.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='flechemano',
    url='https://github.com/flechemano/flechemano',
    packages=find_packages(),
    python_requires='>=3.6',
    package_data={'flechemano': ['install.py']},
    entry_points={
        'console_scripts': [
            'run_install = flechemano.install:main'
        ]
    }
)

