from db import DataBase
import pytest

@pytest.fixture
def data_base():
    database = DataBase()
    return database

def test_save_user(data_base, mocker):
    mock_conn = mocker.patch("sqlite3.connect")
    mock_cursor = mock_conn.return_value.cursor.return_value
    
    data_base.save_user("Om", 30)
    
    mock_conn.assert_called_once_with("usere.db")
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO users (name, age) VALUES (?, ?)", ("Om", 30)
    )