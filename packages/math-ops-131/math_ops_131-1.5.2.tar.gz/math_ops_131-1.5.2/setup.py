from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='math_ops_131',
    version='1.5.2',
    packages=find_packages(),
    description='A Python package for basic mathematical operations.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Unnath Chittimalla',
    license = 'MIT License',
    author_email='unnath.chittimalla@iiitb.ac.in',
    url='https://github.com/AspiringPianist/math_ops_131',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
