from setuptools import setup

name = "types-boltons"
description = "Typing stubs for boltons"
long_description = '''
## Typing stubs for boltons

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`boltons`](https://github.com/mahmoud/boltons) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`boltons`.

This version of `types-boltons` aims to provide accurate annotations
for `boltons==24.0.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/boltons. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `7858e6058b51733f526c6c54035b96a370a12ffc` and was tested
with mypy 1.9.0, pyright 1.1.358, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="24.0.0.20240423",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/boltons.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['boltons-stubs'],
      package_data={'boltons-stubs': ['__init__.pyi', 'cacheutils.pyi', 'debugutils.pyi', 'deprutils.pyi', 'dictutils.pyi', 'easterutils.pyi', 'ecoutils.pyi', 'excutils.pyi', 'fileutils.pyi', 'formatutils.pyi', 'funcutils.pyi', 'gcutils.pyi', 'ioutils.pyi', 'iterutils.pyi', 'jsonutils.pyi', 'listutils.pyi', 'mathutils.pyi', 'mboxutils.pyi', 'namedutils.pyi', 'pathutils.pyi', 'queueutils.pyi', 'setutils.pyi', 'socketutils.pyi', 'statsutils.pyi', 'strutils.pyi', 'tableutils.pyi', 'tbutils.pyi', 'timeutils.pyi', 'typeutils.pyi', 'urlutils.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
