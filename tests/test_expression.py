import pytest
from jsonatago import Jsonata, jeval  # type:ignore

JSONATA_TEST_DATA = """
{
  "Account": {
    "Account Name": "Firefly",
    "Order": [
      {
        "OrderID": "order103",
        "Product": [
          {
            "Product Name": "Bowler Hat",
            "ProductID": 858383,
            "SKU": "0406654608",
            "Description": {
              "Colour": "Purple",
              "Width": 300,
              "Height": 200,
              "Depth": 210,
              "Weight": 0.75
            },
            "Price": 34.45,
            "Quantity": 2
          },
          {
            "Product Name": "Trilby hat",
            "ProductID": 858236,
            "SKU": "0406634348",
            "Description": {
              "Colour": "Orange",
              "Width": 300,
              "Height": 200,
              "Depth": 210,
              "Weight": 0.6
            },
            "Price": 21.67,
            "Quantity": 1
          }
        ]
      },
      {
        "OrderID": "order104",
        "Product": [
          {
            "Product Name": "Bowler Hat",
            "ProductID": 858383,
            "SKU": "040657863",
            "Description": {
              "Colour": "Purple",
              "Width": 300,
              "Height": 200,
              "Depth": 210,
              "Weight": 0.75
            },
            "Price": 34.45,
            "Quantity": 4
          },
          {
            "ProductID": 345664,
            "SKU": "0406654603",
            "Product Name": "Cloak",
            "Description": {
              "Colour": "Black",
              "Width": 30,
              "Height": 20,
              "Depth": 210,
              "Weight": 2
            },
            "Price": 107.99,
            "Quantity": 1
          }
        ]
      }
    ]
  }
}
"""


def test_bool_evaluate():
    expr = Jsonata("$sum(Account.Order.Product.(Price * Quantity)) < 100")
    result = expr.evaluate(JSONATA_TEST_DATA)
    assert result is False


def test_obj_evaluate():
    expr = Jsonata("$.Account")
    result = expr.evaluate(JSONATA_TEST_DATA)
    assert isinstance(result, dict)
    assert result["Account Name"] == "Firefly"


def test_list_evaluate():
    expr = Jsonata("$.Account.Order")
    result = expr.evaluate(JSONATA_TEST_DATA)
    assert isinstance(result, list)
    assert result[0]["OrderID"] == "order103"


def test_float_evaluate():
    expr = Jsonata("$sum(Account.Order.Product.(Price * Quantity))")
    result = expr.evaluate(JSONATA_TEST_DATA)
    assert result == 336.36


def test_int_evaluate():
    expr = Jsonata("$count($.Account)")
    result = expr.evaluate(JSONATA_TEST_DATA)
    assert result == 1


def test_str_evaluate():
    expr = Jsonata("Account.Order[0].OrderID[0]")
    result = expr.evaluate(JSONATA_TEST_DATA)
    assert result == "order103"


def test_no_match_evaluate():
    expr = Jsonata("$xxx")
    result = expr.evaluate(JSONATA_TEST_DATA)
    assert result is None


def test_evaluate_error():
    with pytest.raises(Exception) as exc_info:
        Jsonata("<")
    assert "compilation failed" in str(exc_info.value)


def test_jeval():
    assert 336.36 == jeval(
        JSONATA_TEST_DATA, "$sum(Account.Order.Product.(Price * Quantity))"
    )
