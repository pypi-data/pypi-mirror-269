# Fake Store API Wrapper
## Overview

The Fake Store API Wrapper is a Python library designed to simplify interaction with the Fake Store API. It provides a convenient interface for making API requests, handling responses, and processing data.

## Features

- Easy-to-use interface for accessing Fake Store API endpoints.
- Support for retrieving products, categories, and cart data.
- Flexible parameter options for customizing API requests.
- JSON and XML response format support.

## Installation

You can install the Fake Store API Wrapper using pip:

```bash
pip install fake_store_api_wrapper
```

## Usage

Here's a basic example of how to use the Fake Store API Wrapper:

```python
from fake_store_api_wrapper import FakeStoreAPI

# Create an instance of the API wrapper
api = FakeStoreAPI()

# Retrieve products in a specific category
products = api.products(category="jewelry", sort="asc", limit=10)
print("Products:", products)

# Retrieve carts in a specific date range
carts = api.carts(start_date="2019-02-05", end_date="2019-03-01", sort="asc", limit=10)
print("Carts:", carts)
```

For more detailed usage examples and API documentation, refer to the [documentation](https://fakestoreapi.com/docs).

## Contributing

Contributions are welcome! If you'd like to contribute to the Fake Store API Wrapper, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/my-feature`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature/my-feature`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Jopgood/Fake-Store-API-Wrapper/blob/main/LICENSE) file for details.

## Acknowledgements

- [Fake Store API](https://fakestoreapi.com/) - The API used in this wrapper.
- [Requests](https://docs.python-requests.org/en/latest/) - HTTP library for making requests in Python.

## Support

If you encounter any issues or have questions about the Fake Store API Wrapper, please [open an issue](https://github.com/Jopgood/Fake-Store-API-Wrapper/issues) on GitHub.