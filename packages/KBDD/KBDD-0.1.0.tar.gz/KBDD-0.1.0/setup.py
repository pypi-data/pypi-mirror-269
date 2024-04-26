from setuptools import setup, find_packages

setup(
    name='KBDD',
    version='0.1.0',
    packages=find_packages(),
    description='A package for KBDD: a knowledge-based and data-driven method for genetic network construction',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Chen-Po Liao',
    author_email='liaochenpo@gmail.com',
    license='MIT',
    install_requires=[
        'numpy',
        'scipy',
        'networkx',
        'itertools',
        'random',
        'matplotlib.pyplot',
        'scipy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
