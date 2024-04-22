# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poltergeist']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'poltergeist',
    'version': '0.10.0',
    'description': 'Rust-like error handling in Python, with type-safety in mind.',
    'long_description': '# poltergeist\n\n[![pypi](https://img.shields.io/pypi/v/poltergeist.svg)](https://pypi.python.org/pypi/poltergeist)\n[![versions](https://img.shields.io/pypi/pyversions/poltergeist.svg)](https://github.com/alexandermalyga/poltergeist)\n\n[Rust-like error handling](https://doc.rust-lang.org/book/ch09-00-error-handling.html) in Python, with type-safety in mind.\n\n## Installation\n\n```\npip install poltergeist\n```\n\n## Examples\n\nUse the `@catch` decorator on any function:\n\n```python\nfrom poltergeist import catch\n\n# Handle an exception type potentially raised within the function\n@catch(OSError)\ndef read_text(path: str) -> str:\n    with open(path) as f:\n        return f.read()\n\n# Returns an object of type Result[str, OSError]\nresult = read_text("my_file.txt")\n```\n\nOr wrap errors manually:\n\n```python\nfrom poltergeist import Result, Ok, Err\n\n# Equivalent to the decorated function above\ndef read_text(path: str) -> Result[str, OSError]:\n    try:\n        with open(path) as f:\n            return Ok(f.read())\n    except OSError as e:\n        return Err(e)\n```\n\nThen handle the result in a type-safe way:\n\n```python\n# Get the Ok value or re-raise the Err exception\ncontent: str = result.unwrap()\n\n# Get the Ok value or a default if it\'s an Err\ncontent: str = result.unwrap_or("lorem ipsum")\ncontent: str | None = result.unwrap_or()\n\n# Get the Ok value or compute it from the exception\ncontent: str = result.unwrap_or_else(lambda e: f"The exception was: {e}")\n\n# Get the Err exception or None if it\'s an Ok\nerr: OSError | None = result.err()\n\n# Handle the result using structural pattern matching\nmatch result:\n    case Ok(content):\n        print("Text in upper:", content.upper())\n    case Err(FileNotFoundError() as e):\n        print("File not found:", e.filename)\n```\n\nIt\'s also possible to wrap multiple exception types with the decorator:\n\n```python\n@catch(OSError, UnicodeDecodeError)\ndef read_text(path: str) -> str:\n    with open(path) as f:\n        return f.read()\n```\n\nOr manually:\n\n```python\ndef read_text(path: str) -> Result[str, OSError | UnicodeDecodeError]:\n    try:\n        with open(path) as f:\n            return Ok(f.read())\n    except (OSError, UnicodeDecodeError) as e:\n        return Err(e)\n```\n\nThere is also an async-compatible decorator:\n\n```python\nfrom poltergeist import catch_async\n\n@catch_async(OSError)\nasync def read_text(path: str) -> str:\n    with open(path) as f:\n        return f.read()\n\n# Returns an object of type Result[str, OSError]\nresult = await read_text("my_file.txt")\n```\n\n## Contributing\n\nSet up the project using [Poetry](https://python-poetry.org/):\n\n```\npoetry install\n```\n\nFormat the code:\n\n```\nmake lint\n```\n\nRun tests:\n\n```\nmake test\n```\n\nCheck for typing and format issues:\n\n```\nmake check\n```\n',
    'author': 'Alexander Malyga',
    'author_email': 'alexander@malyga.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/alexandermalyga/poltergeist',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
