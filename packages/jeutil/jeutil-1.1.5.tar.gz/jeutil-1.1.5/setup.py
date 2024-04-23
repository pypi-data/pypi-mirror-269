import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jeutil",
    version="1.1.5",
    author="jeanku, liubing",
    author_email="",
    description="A simple python libs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=["jeutil", "jeutil/Scaffold", "Config"],
    package_data={
        'jeutil': [
            'Scaffold/*.txt'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'configparser',
        'oss2',
    ],
    keywords='util, libs',
    python_requires='>=3',
)
