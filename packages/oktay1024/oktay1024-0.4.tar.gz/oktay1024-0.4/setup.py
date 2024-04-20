from setuptools import setup, find_packages

setup(
    name='oktay1024',
    version='0.4',
    description='A package developed for blacktea024 to integrate it with PyPI.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='flechemano',
    url='https://github.com/flechemano/oktay1024',
    packages=find_packages(),
    install_requires=[
        'pip',
    ],
    python_requires='>=3.6',
)

