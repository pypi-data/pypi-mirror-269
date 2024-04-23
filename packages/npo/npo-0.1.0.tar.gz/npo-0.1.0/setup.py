from setuptools import setup, find_packages

with open("requirements.txt", "r") as fp:
    pkg_requirements = [i.strip() for i in fp.readlines() if len(i.strip()) != 0]


setup(
    name='npo',
    version='0.1.0',
    author='Rajesh Nakka',
    author_email='33rajesh@gmail.com',
    description='Numpy Operations: A simple package for command line operations on numpy arrays',
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=pkg_requirements,
)