from setuptools import setup

name = "types-gevent"
description = "Typing stubs for gevent"
long_description = '''
## Typing stubs for gevent

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`gevent`](https://github.com/gevent/gevent) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`gevent`.

This version of `types-gevent` aims to provide accurate annotations
for `gevent==24.2.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/gevent. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `273e9ea6ddc2d5cad2db7dd25a0383a61be15675` and was tested
with mypy 1.10.0, pyright 1.1.360, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="24.2.0.20240425",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/gevent.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-greenlet', 'types-psutil'],
      packages=['gevent-stubs'],
      package_data={'gevent-stubs': ['__init__.pyi', '_abstract_linkable.pyi', '_config.pyi', '_ffi/__init__.pyi', '_ffi/loop.pyi', '_ffi/watcher.pyi', '_fileobjectcommon.pyi', '_greenlet_primitives.pyi', '_hub_local.pyi', '_hub_primitives.pyi', '_ident.pyi', '_imap.pyi', '_monitor.pyi', '_threading.pyi', '_types.pyi', '_util.pyi', '_waiter.pyi', 'ares.pyi', 'backdoor.pyi', 'baseserver.pyi', 'event.pyi', 'events.pyi', 'exceptions.pyi', 'fileobject.pyi', 'greenlet.pyi', 'hub.pyi', 'libev/__init__.pyi', 'libev/corecext.pyi', 'libev/corecffi.pyi', 'libev/watcher.pyi', 'libuv/__init__.pyi', 'libuv/loop.pyi', 'libuv/watcher.pyi', 'local.pyi', 'lock.pyi', 'monkey.pyi', 'os.pyi', 'pool.pyi', 'pywsgi.pyi', 'queue.pyi', 'resolver/__init__.pyi', 'resolver/ares.pyi', 'resolver/blocking.pyi', 'resolver/cares.pyi', 'resolver/dnspython.pyi', 'resolver/thread.pyi', 'resolver_ares.pyi', 'resolver_thread.pyi', 'select.pyi', 'selectors.pyi', 'server.pyi', 'signal.pyi', 'socket.pyi', 'ssl.pyi', 'subprocess.pyi', 'threadpool.pyi', 'time.pyi', 'timeout.pyi', 'util.pyi', 'win32util.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
