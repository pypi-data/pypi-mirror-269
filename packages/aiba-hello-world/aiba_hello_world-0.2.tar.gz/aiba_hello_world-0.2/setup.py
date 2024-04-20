from setuptools import setup, find_packages

setup(
    name='aiba_hello_world',
    version='0.2',
    packages=find_packages(),
    description='Hello world test package for pypi',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Aiba B',
    author_email='test@test.com',
    url='https://github.com/yourusername/your_package',
    license='MIT',
    install_requires=[
        # Nothing really
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
