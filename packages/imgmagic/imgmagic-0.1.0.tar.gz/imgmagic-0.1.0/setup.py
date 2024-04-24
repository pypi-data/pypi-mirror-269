from setuptools import setup, find_packages



setup(
	name = "imgmagic",
	version = "0.1.0",
	packages = find_packages(),
	install_requires = [
		'numpy==1.23.4',
		'scipy==1.11.4',
		'matplotlib==3.5.1',
		'pillow==9.0.1', 
		'protobuf<4'
	],
)
