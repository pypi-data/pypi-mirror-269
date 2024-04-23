import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="gxr_py_pkg_temp",
  version="0.0.2",
  author="gxr404",
  author_email="gxr40404@gmail.com",
  description="description",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/gxr404/py-pkg-template",
  packages=setuptools.find_packages(),
  classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
)
