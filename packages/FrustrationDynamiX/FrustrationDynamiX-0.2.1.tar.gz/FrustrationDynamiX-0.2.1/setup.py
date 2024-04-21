from setuptools import setup, find_packages

setup(
    name='FrustrationDynamiX',
    version='0.2.1',
    packages=find_packages(),
    description='A package for handling computing frustration in dynamical systems',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ali S. Badereddine',
    author_email='asb24@mail.aub.edu',
    license='MIT',
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'networkx',
        'scipy',
        'ortools',
        'tqdm',
        'pyEDM==1.14.3'
    ],
    python_requires='>=3.6',
    url='https://github.com/asb24repo/FrustrationDynamiX',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
