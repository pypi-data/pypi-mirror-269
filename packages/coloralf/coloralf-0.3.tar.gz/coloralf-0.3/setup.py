from setuptools import setup, find_packages

with open("README.md", "r") as f:
	desc = f.read()

setup(
	name='coloralf',
	version='0.3',
	packages=find_packages(),
	install_requires=[],

	description="Simple package to easy color & transform your console string and output",
	long_description=desc,
	long_description_content_type="text/markdown",
	author="Aexeos - Angelo LF",
	author_email="aexeos413@gmail.com"
)