import setuptools 
  
with open("README.md", "r") as fh: 
    description = fh.read() 
  
setuptools.setup( 
    name="extractstructuresMC", 
    version="1.0.0.1", 
    author="Abhishek Harikrishnan", 
    author_email="abhishek.harikrishnan@fu-berlin.de", 
    packages=["extractStructuresWithMC"], 
    package_dir={'extractStructuresWithMC': 'extractStructuresWithMC'},
    package_data={'extractStructuresWithMC': ['*.bin', 'runTests.py']},
    description="This code is an extension of the neighbor scanning \
    procedure of Moisy & Jiménez (2004), used for the extraction (segmentation)\
    of coherent structures from 3D scalar fields", 
    long_description=description, 
    long_description_content_type="text/markdown", 
    url="https://github.com/Phoenixfire1081/CoherentStructureExtraction", 
    license='MIT', 
    python_requires='>=3.8', 
    install_requires=[] 
) 
