import setuptools

with open("Readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='gits',
    version='0.0.1',
    description='Multi-module wrapper for git',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/briangarydodge/utilities-gits',
    author='Brian Dodge',
    author_email='briangarydodge@gmail.com',
    packages=setuptools.find_packages(),
    install_requires=[
        'pyyaml'
    ],
    zip_safe=False
)