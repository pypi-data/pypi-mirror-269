import setuptools 
  
with open("README.md", "r") as fh: 
    description = fh.read() 
  
setuptools.setup( 
    name="multiLevelPercolation", 
    version="1.0.0.0", 
    author="Abhishek Harikrishnan", 
    author_email="abhishek.harikrishnan@fu-berlin.de", 
    packages=["multiLevelPercolation"], 
    package_dir={'multiLevelPercolation': 'multiLevelPercolation'},
    package_data={'multiLevelPercolation': ['*.bin']},
    description="Identifying individual unique thresholds for structures educed from scalar fields", 
    long_description=description, 
    long_description_content_type="text/markdown", 
    url="https://github.com/Phoenixfire1081/MultiLevelPercolationAnalysis", 
    license='MIT', 
    python_requires='>=3.8', 
    install_requires=[] 
) 
