from unittest.mock import patch, Mock
import requests
import logging
import copy
import pytest

logger = logging.getLogger(__name__)

BASE_URL = "https://myapi.com"

def get_user(user_id):
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    return response

def update_user(user_id, payload):
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=payload)
    return response

def post_user(user_id, payload):
    response = requests.post(f"{BASE_URL}/users/{user_id}", json=payload)
    return response

def delete_user(user_id):
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    return response

# Store payload in a variable
mocked_user_payload = {
    "tasks": [
        {
            "user_id": 1,
            "content": "my first content",
            "task_id": "test_first_related_id",
            "is_done": False
        },
        {
            "user_id": 2,
            "content": "my second content",
            "task_id": "test_second_related_id",
            "is_done": False
        }
    ]
}

add_new_tasks = [
        {
            "user_id": 3,
            "content": "my third content",
            "task_id": "test_third_related_id",
            "is_done": False
        },
        {
            "user_id": 4,
            "content": "my fourth content",
            "task_id": "test_fourth_related_id",
            "is_done": False
        }
    ]

@patch("requests.get")
def test_can_call_endpoint(mock_get):
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mocked_user_payload
    
    mock_get.return_value = mock_response
    
    response = get_user(1)
    
    assert response.status_code == 200


@patch("requests.put")
def test_can_create_task(mock_put):
    updated_payload = copy.deepcopy(mocked_user_payload)
    updated_payload["tasks"][0]["is_done"] = True
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = updated_payload
    
    mock_put.return_value = mock_response
    
    response = update_user(1, updated_payload)
    
    assert response.status_code == 200
    
    logger.info(f"{response.json()}")
    
    assert response.json()["tasks"][0]["is_done"] == True
    
@patch("requests.get")
def test_can_update_task(mock_get):
    
    number = 2
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mocked_user_payload
    
    mock_get.return_value = mock_response
    
    response = get_user(1)
    
    assert response.status_code == 200
    
    payload = response.json()
    tasks = payload["tasks"]
    
    for task in tasks:
        logger.info(f"{task}")
        
    assert len(tasks) == number
    
@pytest.mark.parametrize("new_tasks", add_new_tasks)
# writing a get first because i am using the get first
@patch("requests.get", autospec=True)
@patch("requests.post", autospec=True) # autospec used to give the explicit names
def test_post_new_tasks_in_main_payload(mock_post, mock_get, new_tasks):
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mocked_user_payload
    
    mock_get.return_value = mock_response
    
    response = get_user(1)
    
    assert response.status_code == 200

    updated_payload = copy.deepcopy(mocked_user_payload)
    updated_payload["tasks"].append(new_tasks)
    
    post_response = Mock()
    post_response.status_code = 201
    post_response.json.return_value = updated_payload
    mock_post.return_value = post_response
    
    updated_response = post_user(1, updated_payload)
    
    assert updated_response.status_code == 201
    assert len(updated_response.json()["tasks"]) == 3 # 4 will not come because parameterize function will add the new data one by one
    
    logger.info(f"{updated_response.json()}")
    
    
@patch("requests.get", autospec=True)
@patch("requests.delete",autospec=True)
def test_can_delete_some_task_in_payload(mock_delete, mock_get):
    delete_response = Mock()
    delete_response.status_code = 200
    delete_response.json.return_value = mocked_user_payload
    
    mock_delete.return_value = delete_response
    
    final_response = delete_user(2)
    
    assert final_response.status_code == 200 
    # Now simulate GET returning 404 (because item was deleted)
    mock_get_response = Mock()
    mock_get_response.status_code = 404
    mock_get_response.json.return_value = {"error": "User not found"}
    mock_get.return_value = mock_get_response
    
    # Call GET after DELETE
    get_response = get_user(2)
    assert get_response.status_code == 404
    logger.info(f"the data is: {get_response.json()}")