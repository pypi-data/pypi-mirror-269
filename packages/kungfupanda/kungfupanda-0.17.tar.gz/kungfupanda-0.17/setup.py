from setuptools import setup, find_packages
from setuptools.command.install import install


class CustomInstallCommand(install):
    def run(self):
        print("Congratulations! You've successfully installed kungfupanda from PyPI.")
        install.run(self)


setup(
    name='kungfupanda',
    version='0.17',
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
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
    cmdclass={
        'install': CustomInstallCommand,
    }
)
