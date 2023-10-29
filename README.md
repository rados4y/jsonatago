# jsonatago: JSONata for Python
jsonatago is a Python library that enables you to evaluate JSONata expressions. This project aims to bring the power and flexibility of JSONata to Python developers.

## Credits
This project uses the Go implementation of JSONata from jsonata-go. All credit for the Go implementation goes to the authors and contributors of jsonata-go.

## Installation
To install jsonatago, you can use pip:

``` bash
pip install jsonatago
```

## Usage
Here's a simple example that demonstrates how to evaluate a JSONata expression:

python
``` python
from jsonatago import Jsonata

JSONATA_TEST_DATA = {
    "Account": {
        "Order": [
            {"Product": [{"Price": 10, "Quantity": 2}, {"Price": 5, "Quantity": 5}]},
            {"Product": [{"Price": 20, "Quantity": 1}, {"Price": 15, "Quantity": 3}]}
        ]
    }
}
expr = Jsonata("$sum(Account.Order.Product.(Price * Quantity))")
print(expr.evaluate(JSONATA_TEST_DATA))
```

This will output the sum of all Price * Quantity for each product in each order.

You can use as well direct method for compilation and evaluation in one step.
python
``` python
from jsonatago import jeval

JSONATA_TEST_DATA = {
    "Account": {
        "Order": [
            {"Product": [{"Price": 10, "Quantity": 2}, {"Price": 5, "Quantity": 5}]},
            {"Product": [{"Price": 20, "Quantity": 1}, {"Price": 15, "Quantity": 3}]}
        ]
    }
}
print(jeval(JSONATA_TEST_DATA,"$sum(Account.Order.Product.(Price * Quantity))"))
```

## Contributing
If you'd like to contribute to this project, please feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.