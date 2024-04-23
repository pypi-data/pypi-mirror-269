from setuptools import setup, find_packages

setup(
    name='panorimage',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        #  'numpy >= 1.13.3'
    ],
    author='r1ddy16',
    author_email='r1ddy16@gmail.com',
    description='Definition of panoramic image or normal image.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown', 
    url='https://https://github.com/r1ddy16/Panorimage',
)
