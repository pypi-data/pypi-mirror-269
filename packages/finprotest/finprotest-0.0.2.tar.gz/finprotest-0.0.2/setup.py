import setuptools


setuptools.setup(
    name="finprotest", # Replace with your own username
    version="0.0.2",
    author="Finpro",
    author_email="finpro1224@gmail.com",
    description="test package",
    readme = "README.md",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6')