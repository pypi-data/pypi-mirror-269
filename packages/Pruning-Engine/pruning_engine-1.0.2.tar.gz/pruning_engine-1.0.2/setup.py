import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Pruning_Engine",                     # This is the name of the package
    version="1.0.2",                        # The initial release version
    author="Zhenyu Lin",                     # Full name of the author
    description="Pruning Engine for CNN",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.9',                # Minimum version requirement of the package
    py_modules=["Pruning_engine"],             # Name of the python package
    package_dir={'':'Pruning_Engine/src'},     # Directory of the source code of the package
    install_requires=[
        "numpy",
        "Pillow",
        "PyYAML",
        "scikit_learn",
        "thop",
        "torch",
        "torchvision",
        "tqdm",

    ]                     
)