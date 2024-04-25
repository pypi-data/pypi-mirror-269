import setuptools 

with open("README.md", "r") as fh: 
	long_description = fh.read() 

setuptools.setup( 
	name="summers_pack", 

	version="0.0.1", 

	author="Ansh Gupta", 

	author_email="Ansh.Gupta@iiitb.ac.in", 

	description="For doing calculations like Addition, Multiplication and Subtraction", 

	long_description=long_description, 
	long_description_content_type="text/markdown", 

	packages=setuptools.find_packages(), 


	license="MIT", 

	classifiers=[ 
		"Programming Language :: Python :: 3", 
		"License :: OSI Approved :: MIT License", 
		"Operating System :: OS Independent", 
	],
	python_requires='>=3.6', 
) 
