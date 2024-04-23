import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pylint-sonarjson-catlab",
    version="2.0.0",
    author="Teake Nutma, Topin2001",
    description="A PyLint plugin that can output to SonarQube-importable JSON",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cnescatlab/pylint-sonarjson-catlab ",
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    license_file='LICENSE',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "pylint-plugin-utils>=0.7",
        "pylint>=3.0.0,<4"
    ],
)
