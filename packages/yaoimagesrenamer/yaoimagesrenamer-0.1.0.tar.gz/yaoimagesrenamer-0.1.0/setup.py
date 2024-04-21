from setuptools import setup, find_packages

setup(
    name='yaoimagesrenamer',  # Name of your package
    version='0.1.0',  # Version of your package
    description='images renamer',  # Short description
    url='https://github.com/BladeRunnerYao/yaoimagesrenamer',  # Project's URL
    packages=find_packages(),  # Packages to include in the distribution
    classifiers=[  # Classifiers for PyPI
        'Development Status :: 3 - Alpha',  # Project's development status
        'Intended Audience :: Developers',  # Intended audience
        'Programming Language :: Python :: 3.9',  # Compatible Python versions
        'License :: OSI Approved :: MIT License',  # Project's license
    ],
    install_requires=[  # Dependencies required to install your package
        'numpy',  # Example dependency
    ],
    include_package_data=True,  # Include non-code files from MANIFEST.in
    python_requires='>=3.8',  # Minimum Python version required
)
