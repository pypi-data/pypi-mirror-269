# setup.py
 
from setuptools import setup, find_packages
 
setup(
    name='aadharverify',
    version='0.1',
    packages=find_packages(),
    description='A library that verifies the aadhar',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ritesh Rout',
    author_email='x21127069@student.ncirl.ie',
    license='MIT',
    install_requires=[],
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