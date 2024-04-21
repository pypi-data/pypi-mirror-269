from setuptools import setup, find_packages

setup(
    name='FrustrationDynamiX',
    version='0.1.0',
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
        'python-ortools',
        'tqdm',
        'pyEDM==1.14.3',
        'shutilwhich', # if shutil is required, it's part of the standard library and doesn't need to be installed
        'warnings' # warnings is also part of the standard library
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
