import setuptools 
  
with open("README.md", "r") as fh: 
    description = fh.read() 
  
setuptools.setup( 
    name="percolationAnalysis", 
    version="1.0.0.1", 
    author="Abhishek Harikrishnan", 
    author_email="abhishek.harikrishnan@fu-berlin.de", 
    packages=["percolationAnalysis"], 
    package_dir={'percolationAnalysis': 'percolationAnalysis'},
    package_data={'percolationAnalysis': ['*.bin']},
    description="Identifying non-subjective thresholds for scalar indicators of coherent structures with percolation analysis", 
    long_description=description, 
    long_description_content_type="text/markdown", 
    url="https://github.com/Phoenixfire1081/PercolationAnalysis", 
    license='MIT', 
    python_requires='>=3.8', 
    install_requires=[] 
) 
