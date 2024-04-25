from setuptools import setup

name = "types-JACK-Client"
description = "Typing stubs for JACK-Client"
long_description = '''
## Typing stubs for JACK-Client

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`JACK-Client`](https://github.com/spatialaudio/jackclient-python) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`JACK-Client`.

This version of `types-JACK-Client` aims to provide accurate annotations
for `JACK-Client==0.5.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/JACK-Client. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `273e9ea6ddc2d5cad2db7dd25a0383a61be15675` and was tested
with mypy 1.10.0, pyright 1.1.360, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="0.5.10.20240425",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/JACK-Client.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-cffi', 'numpy>=1.20'],
      packages=['jack-stubs'],
      package_data={'jack-stubs': ['__init__.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
