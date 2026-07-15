import pytest
from main import process_orders


#---------------ა
def test_product_not_found():
    orders: list[dict[str, str | int]] = [
        {"product": "banana", "quantity": 2},
        {"product": "apple", "quantity": 4}
    ]
    
    inventory: dict[str, int] = {
        "apple": 15,
        "mango": 32
    }

    with pytest.raises(ValueError, match="Product 'banana' not found in inventory"):
        process_orders(orders=orders, inventory=inventory)

#---------------ბ
def test_product_quantity_not_enough():
    orders: list[dict[str, str | int]] = [
        {"product": "banana", "quantity": 10},
        {"product": "apple", "quantity": 4}
    ]
    
    inventory: dict[str, int] = {
        "apple": 15,
        "mango": 32,
        "banana": 5
    }

    with pytest.raises(ValueError, match="Not enough stock for 'banana'"):
        process_orders(orders=orders, inventory=inventory)


#---------------გ
def test_successful_order():
    orders: list[dict[str, str | int]] = [
        {"product": "apple", "quantity": 3}
    ]

    inventory: dict[str, int] = {
        "apple": 10
    }

    result = process_orders(orders, inventory)

    assert result == orders

    assert inventory["apple"] == 7