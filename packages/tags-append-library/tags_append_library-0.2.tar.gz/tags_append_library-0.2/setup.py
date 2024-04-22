import io
from setuptools import setup, find_packages

with io.open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='tags_append_library',
    version='0.2',
    packages=find_packages(),
    # install_requires=[
        # Add any dependencies here if required
    # ],
    description='A library to append viral tags to posts automatically',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
