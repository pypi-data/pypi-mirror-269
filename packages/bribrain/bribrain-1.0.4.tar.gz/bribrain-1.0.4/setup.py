from setuptools import setup, find_packages

VERSION = '1.0.4'
DESCRIPTION = 'Standard code for Dept BRIBrain'

# Setting up
setup(
    name="bribrain",
    version=VERSION,
    author="Andri Ariyanto",
    author_email="ariyant.andri@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['mysql-connector-python==8.0.28', 'psycopg2'],
    keywords=['python', 'ddb', 'bribrain', 'andri', 'gondrol'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)