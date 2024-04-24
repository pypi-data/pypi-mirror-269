from setuptools import setup, find_packages

setup(
    name='ticker_feeder',
    version='0.2.1',
    description='A simple data feeding library',
    author='Sravan Peesu',
    author_email=' sravanpeesu@gmail.com',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
