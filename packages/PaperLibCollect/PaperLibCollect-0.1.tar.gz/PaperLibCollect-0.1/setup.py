from distutils.core import setup
import pathlib
import setuptools

setuptools.setup(
    name='PaperLibCollect',
    version='0.1',
    description='Collective python packages from papers',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://google.com',
    author='Author Name', 
    author_email='author_email@mail.com',
    license='The Unlicense',
    projects_urls={
        "Documentation": "x",
        "Source": "https://github.com"
    },
    python_requires=">3.9,<3.12",
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["paper = paper.cli:main"]},

)
