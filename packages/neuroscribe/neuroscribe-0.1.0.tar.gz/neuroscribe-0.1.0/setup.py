import os

from setuptools import find_packages, setup


# TODO: Update setup.py to handle mps configuration
def cuda_available():
    return 'CUDA_PATH' in os.environ or 'CUDA_HOME' in os.environ


install_requires = ['numpy==1.26.4']
if cuda_available():
    install_requires.extend(['cupy-cuda12x==13.0.0', 'fastrlock==0.8.2',])


setup(
    name='neuroscribe',
    version='0.1.0',
    author='Ghaith Husrieh',
    author_email='Ghaith.Husrieh.01@gmail.com',
    description='NeuroScribe - a lightweight deep learning framework.',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
    install_requires=install_requires
)
