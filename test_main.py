from main import PracticeCode, UserManager, DataBase, CheckPrimeNumber, MockTest
import pytest

@pytest.fixture
def practice_code():
    return PracticeCode()

def test_get_weather(practice_code):
    assert practice_code.get_weather(21) == "hot"

def test_add(practice_code):
    assert practice_code.add(2, 3) == 5
    assert practice_code.add(-1, 1) == 0
    assert practice_code.add(5, 2) == 8

def test_divide(practice_code):
    with pytest.raises(ValueError, match="Cannot divide with zero"):
        practice_code.divide(10, 0)
        
@pytest.fixture
def user_manager():
    """ Create a fresh instance of UserManager before the test """
    return UserManager()

# If we do not use fixture and use as below
# user_manager = UserManager()
# Then it will store the user with test_add_user and then it will fail for test_add_duplicate_user
# because instance will store the value and it will not restart so better to use the fixture

def test_add_user(user_manager):
    assert user_manager.add_user("John_Doe", "John@example.com") == True
    assert user_manager.get_user("John_Doe") =="John@example.com"

def test_add_duplicate_user(user_manager):
    user_manager.add_user("John_Doe", "John@example.com")
    with pytest.raises(ValueError):
        user_manager.add_user("John_Doe", "John@example.com")
        

@pytest.fixture
def data_base():
    database = DataBase() # Provide the fixture instance
    yield database  # Cleanup setup (not needed for in-memory, but useful for real DBs)
    database.data.clear()

def test_add_user_id(data_base):
    data_base.add_data_user(1, "Om")
    assert data_base.get_data_user(1) == "Om"

def test_add_duplicate_user_id(data_base):
    data_base.add_data_user(1, "Om")
    with pytest.raises(ValueError, match="User already exsists"):
        data_base.add_data_user(1, "Namha")

def test_delete_user_id(data_base):
    data_base.add_data_user(2, "Namha")
    data_base.delete_data_user(2)
    assert data_base.get_data_user(2) is None 
    
@pytest.fixture
def check_prime_number():
    return CheckPrimeNumber()

list_number = [
    (1, False),
    (2, True),
    (3, True),
    (4, False),
    (17, True),
    (18, False),
    (19, True),
    (25, False)
]

@pytest.mark.parametrize("num, expected", list_number)
def test_prime_number(check_prime_number, num, expected):
    assert check_prime_number.is_prime(num) == expected
    

@pytest.fixture
def mock_test():
    mocktest = MockTest()
    return mocktest

def test_get_weather_from_api(mock_test, mocker):
    # Mock request.get
    # main.requests.get = main.py file then requests from import and get message
    mock_get = mocker.patch("main.requests.get")
    
    #Set return values
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"temperature": 25, "condition": "Sunny"}
    
    # Call function
    result = mock_test.get_weather_from_api("Dubai")
    
    assert result == {"temperature": 25, "condition": "Sunny"}
    mock_get.assert_called_once_with("https://api.weather.com/v1/Dubai")