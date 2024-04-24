from setuptools import setup, find_packages

setup(
    name='kungfupanda',
    version='0.22',
    author='The Big Fat Panda',
    author_email='po_the_big_fat_panda@gmail.com',
    description="A simple package to make everything easy for programmers to do everything the cool way",
    long_description="""A simple package for people who are not bound by societal rules, made by a cute panda trained to be a dragon warrior. For the full story, watch the original trilogy:
    - Kung Fu Panda 1
    - Kung Fu Panda 2
    - Kung Fu Panda 3
    """,
    url='',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas',
        'opencv-python'
    ],
    
)
