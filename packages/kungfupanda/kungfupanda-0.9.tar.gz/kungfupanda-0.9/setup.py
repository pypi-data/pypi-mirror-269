from setuptools import setup, find_packages


setup(
    name='kungfupanda',
    version='0.9',
    author='The big fat panda',
    author_email='po_the_big_fat_panda@gmail.com',
    description="A simple package to make everything easy for programmers for doing everything the cool way",
    long_description="""A simple package for the people who are not bound by society rules 
    made by an cute panda who trained to be a dragon warrior
    For all the story watch the original triology
    Kung Fu Panda 1
    Kung Fu Panda 2
    Kung Fu Panda 3
    """,
    url='',
    packages=find_packages(where='my_package'),
    install_requires=[
        'requests>=2.25.1',
        'numpy>=1.21.0',
        'pandas>=2.2.2',
    ],
    setup_requires=['wheel'],

)