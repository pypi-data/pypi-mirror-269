from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='passwork',
    version='0.0.1',
    author='dimavladimirov',
    author_email='vladimirovdmitry@mail.ru',
    description='Passwork connector',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/dimavladimirov/passwork',
    packages=find_packages(),
    install_requires=[
        'requests>=2.31.0',
        'cryptography>=42.0.5',
        'loguru>=0.7.2'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='example python',
    project_urls={
        'Documentation': 'https://passwork.ru/help/'
    },
    python_requires='>=3.10'
)
