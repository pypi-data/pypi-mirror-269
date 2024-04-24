from setuptools import setup

setup(
    name='gleweather',
    version='0.1.3',
    description="A python package aiming to allow you to use google's weather service with automatic city detection "
                "without having to search for hours to learn how to do it.",
    url='https://github.com/Pohie/gleweather-py.git',
    author='Abbott Broughton',
    author_email='abbottbroughton@icloud.com',
    license='The Unlicense',
    packages=['gleweather'],
    install_requires=['requests', 'bs4'],
    long_description='You can use gleweather.weather() to get the weather where you currently are.',

    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)