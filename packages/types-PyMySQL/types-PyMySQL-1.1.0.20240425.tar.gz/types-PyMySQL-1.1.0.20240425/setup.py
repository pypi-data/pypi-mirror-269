from setuptools import setup

name = "types-PyMySQL"
description = "Typing stubs for PyMySQL"
long_description = '''
## Typing stubs for PyMySQL

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`PyMySQL`](https://github.com/PyMySQL/PyMySQL) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`PyMySQL`.

This version of `types-PyMySQL` aims to provide accurate annotations
for `PyMySQL==1.1.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/PyMySQL. All fixes for
types and metadata should be contributed there.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `273e9ea6ddc2d5cad2db7dd25a0383a61be15675` and was tested
with mypy 1.10.0, pyright 1.1.360, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="1.1.0.20240425",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/PyMySQL.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['pymysql-stubs'],
      package_data={'pymysql-stubs': ['__init__.pyi', 'charset.pyi', 'connections.pyi', 'constants/CLIENT.pyi', 'constants/COMMAND.pyi', 'constants/CR.pyi', 'constants/ER.pyi', 'constants/FIELD_TYPE.pyi', 'constants/FLAG.pyi', 'constants/SERVER_STATUS.pyi', 'constants/__init__.pyi', 'converters.pyi', 'cursors.pyi', 'err.pyi', 'times.pyi', 'util.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
