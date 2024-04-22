from setuptools import setup, find_packages

setup(
    name='solver-multiRPC',
    version='2.0.1',
    author="rorschach",
    author_email='rorschach45001@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='multiRPC solver',
    url='https://github.com/SYMM-IO/solver-multiRPC.git',
    install_requires=[
        'requests',
    ],

)