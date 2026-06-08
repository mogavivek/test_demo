import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from shopping_cart import ShoppingCart, TestMath
from item_database import ItemDatabase
from unittest.mock import Mock
from datetime import datetime
import pytest
import logging
import math

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")  # module means want to run one time per module, means run ones per file
def cart():
    cart = ShoppingCart(5)
    cart.add_item("apple")
    logger.info("Apple item added in the list")
    yield cart
    cart.clear_all_item()
    logger.info("clear the list")


@pytest.mark.usefixtures("cart")
def test_add_item_in_list(cart):
    assert cart.item_size() == 1


@pytest.mark.parametrize("item_1, item_2, expected_total", 
                         [("orange", "banana", 3),
                          ("grapes", "Mango", 5),
                          ("Pineapple", "Watermelon", 9)] # This one will fail because it should be 7 not 9
                         )
def test_add_item_as_input_field_in_list(cart, item_1, item_2, expected_total):
    cart.add_item(item_1)
    cart.add_item(item_2)
    assert cart.item_size() == expected_total, \
        "Actual and expected Total do not Match"
      
    
def test_item_present_in_cart(cart):
    cart.add_item("apple")
    assert "apple" in cart.get_items()
    
    
@pytest.mark.skip(reason="Test will always fail so that is wh skipping")
def test_when_add_more_than_max_items_should_fail(cart):
    for _ in range(5):
        cart.add_item("apple")
    
    with pytest.raises(OverflowError):
        cart.add_item("apple")

@pytest.mark.skip
def test_get_total_item_price(cart):
    # cart = ShoppingCart(5)    not required because we have put it into the common function
    cart.add_item("apple")
    cart.add_item("orange")
    
    item_database = ItemDatabase()
    
    def mock_get_item(item:str):
        if item == "apple":
            return 1.0
        if item == "orange":
            return 2.0
    
    item_database.get = Mock(side_effect=mock_get_item)
    
    assert cart.get_total_price(price_map=item_database) == 3.0


# parametrize with 2 decoratores
@pytest.mark.parametrize("base", [1, 2, 3])
@pytest.mark.parametrize("exponent", [4, 5, 6]) # in this it will run 9 times, because 4 will take 1,2,3 same 5 will take 1,2,3 and 6 will take 1,2,3
def test_raising_base_to_power(base, exponent):
    result = base ** exponent
    assert result == math.pow(base, exponent)


# Parametrize pytest with fixtuers
@pytest.fixture(params=["add_one_item", "add_two_item", "add_three_item"])
def initialize_list(request):
    cart = ShoppingCart(5)
    if request.param == "add_one_item":
        cart.add_item("Banana")
    elif request.param == "add_two_item":
        cart.add_item("Banana")
        cart.add_item("Mango")
    elif request.param == "add_three_item":
        cart.add_item("Banana")
        cart.add_item("Mango")
        cart.add_item("Grapes")
    
    request.cls.cart = cart
    logger.info(f"Selected param: {request.param}")
    
    yield cart
    cart.clear_all_item()
    logger.info("All item has been removed from the list")
        
@pytest.mark.usefixtures("initialize_list")
class BaseClass:
    pass

class Test_List(BaseClass):
    def test_multiple_add_item_in_list(self):
        assert self.cart.item_size() > 0
        

@pytest.mark.skipif(
    datetime.now() <= datetime(2099, 12, 31),
    reason="Repo is not complete until after finishing other tests"
    )
def test_add_item_in_list(cart):
    assert cart.item_size() == 1

# xfail and stop pytest tests
def test_devide_number():
    num_1, num_2 = TestMath.take_two_numbers()
    pytest.xfail("Need to investigate why it is failing")
    result = num_1 + num_2
    assert result == num_1 / num_2
    
@pytest.mark.xfail(reason="Result add numbers and not multiply numbers")
def test_square_number():
    num_1, num_2 = TestMath.take_two_numbers()
    result = num_1 + num_2
    assert result == num_1 * num_2
    
@pytest.mark.xfail(reason="Result add numbers are both the correct")
def test_square_number_work():
    num_1, num_2 = TestMath.take_two_numbers()
    result = num_1 * num_2
    assert result == num_1 * num_2
    
@pytest.mark.xfail(run=True)
def test_cube_number():
    num_1, num_2 = TestMath.take_two_numbers()
    result = num_1 * num_2 * num_1
    assert result == num_1 * num_2 * num_1

# So the below testcase will fail because it needs to be assert should fail
@pytest.mark.xfail(run=False)
def test_cube_number_fail():
    num_1, num_2 = TestMath.take_two_numbers()
    result = num_1 * num_2 * num_1
    assert result == num_1 * num_2 * num_1
    
