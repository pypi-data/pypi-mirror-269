from setuptools import setup, find_packages

with open("README.md", "r") as f:
	desc = f.read()

setup(
	name='coloralf',
	version='0.2',
	packages=find_packages(),
	install_requires=[],

	long_description=desc,
	long_description_content_type="text/markdown"
)