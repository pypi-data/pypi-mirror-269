from setuptools import setup, find_packages

setup(
    name='animatebar',
    version='1.0',
    author='Ranjit Maity',
    description='A Python package to generate animated bar plots with Plotly',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'plotly>=4.0.0',
        'numpy>=1.0.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
