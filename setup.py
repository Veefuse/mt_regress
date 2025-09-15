
# setup.py

from setuptools import setup, find_packages

setup(
    name='mt_regress',
    version='1.0.1',
    author='wang tank',
    description='a regress test tool',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'run_regress = mt_regress.run_regress:main',
            'build_regress = mt_regress.build_regress:main',
        ],
    },
    install_requires=[
        'pyyaml',
    ],
)