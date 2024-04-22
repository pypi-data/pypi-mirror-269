import setuptools

with open("README.md", "r") as fh: 
    description = fh.read() 
  
setuptools.setup( 
    name="sequrekey_pkg", 
    version="0.0.1", 
    author="7399", 
    author_email="", 
    packages=["sequrekey_pkg"], 
    description="A sample SequreKey package", 
    long_description=description, 
    long_description_content_type="text/markdown", 
    url="", 
    license='MIT', 
    python_requires='>=3.12', 
    install_requires=[] 
) 