from setuptools import setup, find_packages

setup(
    name='SnaxModule',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'os',
        'requests'
    ],
    author='Snax Dev',
    author_email='lijisp04@gmail.com',
    description='Bring Colors to CLI Make It Fun',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your_username/my_library',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)