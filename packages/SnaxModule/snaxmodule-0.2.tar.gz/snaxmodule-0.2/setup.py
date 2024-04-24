from setuptools import setup, find_packages

setup(
    name='SnaxModule',
    version='0.2',  # Increased version number
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    author='Snax Dev',
    author_email='lijisp04@gmail.com',
    description='Bring Colors to CLI Make It Fun Edwin',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your_username/SnaxModule',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
