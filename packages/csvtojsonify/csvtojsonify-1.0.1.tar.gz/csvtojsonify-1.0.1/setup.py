from setuptools import setup, find_packages

setup(
    name='csvtojsonify',
    version='1.0.1',
    author='csvtojsonify',
    author_email='sriramsreedhar003@gmail.com',
    description='A Python script to convert CSV to JSON',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/sriramsreedhar/csvtojsonify',
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
