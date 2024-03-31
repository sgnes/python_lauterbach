import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python_lauterbach", # Replace with your own username
    version="0.0.1",
    author="Guopeng Sun",
    author_email="sgnes0514@gmai.com",
    description="Python Lauterbach Automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sgnes/python_lauterbach",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'lauterbach-trace32-rcl ',
      ],
    python_requires='>=3.6',
)