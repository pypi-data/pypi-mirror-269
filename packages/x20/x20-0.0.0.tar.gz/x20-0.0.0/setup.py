from setuptools import setup, find_packages

setup(
    name="x20",
    version="0.0.0",
    author="Dongqi Su",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=["x20"],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.12.0",
)
