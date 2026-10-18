import pytest
from fastapi.testclient import TestClient

import main_app as application

@pytest.fixture
def client(tmp_path, monkeypatch):
    # Give each test an independent temporary database.
    test_db = tmp_path / "test_sensor.db"
    
    monkeypatch.setattr(application, "DB_PATH", test_db)
    application.init_db()
    
    with TestClient(application.app) as test_client:
        yield test_client