import setuptools

version = "0.0.2a6"


install_requires = [
    "pydantic",
    "certifi>=2023.7.22",
    "charset-normalizer>=3.2.0",
    "dataclasses-json>=0.6.1",
    "idna>=3.4",
    "jsonpath-python>=1.0.6 ",
    "marshmallow>=3.19.0",
    "mypy-extensions>=1.0.0",
    "packaging>=23.1",
    "python-dateutil>=2.8.2",
    "requests>=2.31.0",
    "six>=1.16.0",
    "typing-inspect>=0.9.0",
    "typing_extensions>=4.7.1",
    "urllib3>=1.26.18",
]


# https://packaging.python.org/tutorials/packaging-projects/
setuptools.setup(
    name="gantry-logger",
    version=version,
    install_requires=install_requires,
    include_package_data=True,
    author="Gantry Systems, Inc.",
    author_email="oss@gantry.io",
    description="Gantry Python Library",
    long_description="",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    license="Apache Software License v2",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
