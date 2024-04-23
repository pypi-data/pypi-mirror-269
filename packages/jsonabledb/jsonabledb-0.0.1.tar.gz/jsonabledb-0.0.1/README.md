# jsonableDB

[![GitHub][github_badge]][github_link] [![PyPI][pypi_badge]][pypi_link]

**jsonableDB** is a lightweight document-oriented database based on JSON.



## Installation

```bash
pip install jsonabledb
```



## Quickstart

```python
import jsonable

client = jsonable.Client("path")

collection = client["database_name"]["collection_name"]

collection.find()
```



## License

**jsonableDB** has a BSD-3-Clause license, as found in the [LICENSE](https://github.com/imyizhang/jsonabledb/blob/main/LICENSE) file.



## Contributing

Thanks for your interest in contributing to **jsonableDB**! Please feel free to create a pull request.



## Changelog

**jsonableDB 0.0.1**

* Initial release





[github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label
[github_link]: https://github.com/imyizhang/jsonabledb



[pypi_badge]: https://badgen.net/pypi/v/jsonabledb?icon=pypi&color=black&label
[pypi_link]: https://www.pypi.org/project/jsonabledb