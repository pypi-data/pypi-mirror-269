from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ticker_feeder',
    version='0.2.2',
    description='The "Ticker Feeder" Python package provides a straightforward and efficient way to handle data feeding operations.',
    long_description=long_description,
    long_description_content_type='text/markdown',  # This is important if your README is in markdown
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