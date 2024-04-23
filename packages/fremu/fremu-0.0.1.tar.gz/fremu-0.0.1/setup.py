import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fremu",
    version="0.0.1",
    author="Jiachen Bai",
    author_email="astrobaijc@gmail.com",  
    description="Emulator for f(R) gravity",
    long_description=long_description, 
    long_description_content_type="text/markdown",
    url="https://github.com/astrobai/fremu",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
