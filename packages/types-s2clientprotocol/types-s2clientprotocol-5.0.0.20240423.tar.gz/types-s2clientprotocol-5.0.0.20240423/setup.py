from setuptools import setup

name = "types-s2clientprotocol"
description = "Typing stubs for s2clientprotocol"
long_description = '''
## Typing stubs for s2clientprotocol

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`s2clientprotocol`](https://github.com/Blizzard/s2client-proto) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`s2clientprotocol`.

This version of `types-s2clientprotocol` aims to provide accurate annotations
for `s2clientprotocol==5.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/s2clientprotocol. All fixes for
types and metadata should be contributed there.

Partially generated using [mypy-protobuf==3.6.0](https://github.com/nipunn1313/mypy-protobuf/tree/v3.6.0) and libprotoc 3.6.1 on [s2client-proto 5.0.12.91115.0](https://github.com/Blizzard/s2client-proto/tree/c04df4adbe274858a4eb8417175ee32ad02fd609)

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `7858e6058b51733f526c6c54035b96a370a12ffc` and was tested
with mypy 1.9.0, pyright 1.1.358, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="5.0.0.20240423",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/s2clientprotocol.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-protobuf'],
      packages=['s2clientprotocol-stubs'],
      package_data={'s2clientprotocol-stubs': ['build.pyi', 'common_pb2.pyi', 'data_pb2.pyi', 'debug_pb2.pyi', 'error_pb2.pyi', 'query_pb2.pyi', 'raw_pb2.pyi', 'sc2api_pb2.pyi', 'score_pb2.pyi', 'spatial_pb2.pyi', 'ui_pb2.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
