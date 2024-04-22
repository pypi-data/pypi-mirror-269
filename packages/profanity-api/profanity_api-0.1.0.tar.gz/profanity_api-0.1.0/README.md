# A Python client for profanity.dev's API

[![PyPi](https://img.shields.io/pypi/dm/profanity-api?label=Downloads&logo=pypi)](https://pypi.org/project/profanity-api)
[![License](https://img.shields.io/pypi/l/profanity-api?color=orange&style=flat-square)](https://github.com/nwithan8/profanity-python/blob/master/LICENSE)

[![Open Issues](https://img.shields.io/github/issues-raw/nwithan8/profanity-python?color=gold&style=flat-square)](https://github.com/nwithan8/profanity-python/issues?q=is%3Aopen+is%3Aissue)
[![Closed Issues](https://img.shields.io/github/issues-closed-raw/nwithan8/profanity-python?color=black&style=flat-square)](https://github.com/nwithan8/profanity-python/issues?q=is%3Aissue+is%3Aclosed)
[![Latest Release](https://img.shields.io/github/v/release/nwithan8/profanity-python?color=red&label=latest%20release&logo=github&style=flat-square)](https://github.com/nwithan8/profanity-python/releases)

[![Discord](https://img.shields.io/discord/472537215457689601?color=blue&logo=discord&style=flat-square)](https://discord.gg/7jGbCJQ)
[![Twitter](https://img.shields.io/twitter/follow/nwithan8?label=%40nwithan8&logo=twitter&style=flat-square)](https://twitter.com/nwithan8)

Interact with [profanity.dev](https://profanity.dev)'s API

# Installation

- From PyPi: ``python -m pip install profanity-api``

# Usage

This client allows you to send messages to profanity.dev's API for analysis. Results include a boolean value for whether
the message contains profanity, and a confidence score for the prediction.

Import the ``profanity_api`` package as initialize the API
Example:

```python
import profanity_api

results = profanity_api.is_profane(message="This is the message to test")

print(results.is_profane)
print(results.confidence)
```
