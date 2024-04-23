import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='uptycs-py',
     version='0.0.3',
     author="Julian Wayte",
     author_email="jwayte@uptycs.com",
     description="Uptycs API helper library (for Python 3)",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/Uptycs/uptycs-py",
     install_requires=[
        'requests',
        'PyJWT >= 0.5.2',
     ],
     packages = ["uptycs_py"],
     package_data={"": ["LICENSE"]},
     package_dir={"uptycs_py": "src/uptycs_py"},
     include_package_data=True,
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
