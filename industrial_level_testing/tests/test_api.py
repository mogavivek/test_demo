import pytest
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_health_endpoint(client):
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
   
    
def test_create_and_add_sensor(client):
    payload = {
        "name": "Pump-01",
        "temperature": 65.5,
        "status": "online"
    }
    
    response = client.post("/api/sensors", json=payload)
    
    logger.info(f"The post response is: {response.json()}")
    
    assert response.status_code == 201
    created = response.json()
    assert created["name"] == "Pump-01"
    assert created["temperature"] == 65.5
    
    read_response = client.get(f"/api/sensors/{created['id']}")
    
    logger.info(f"The read response is: {read_response}")
    
    assert read_response.status_code == 200
    assert read_response.json()["status"] == "online"
    

def test_duplicate_sensor_is_rejected(client):
    payload = {
        "name": "Pump-02",
        "temperature": 60,
        "status": "online",
    }
    
    assert client.post("/api/sensors", json=payload).status_code == 201
    
    response = client.post("/api/sensors", json=payload)
    
    assert response.status_code == 409
    
@pytest.mark.parametrize("temperature", [-51, 251])
def test_out_of_range_temperature_is_rejected(client, temperature):
    response = client.post(
        "/api/sensors",
        json={
            "name": "Invalid-Pump",
            "temperature": temperature,
            "status": "online"
        }
    )
    
    assert response.status_code == 422


def test_missing_sensor_returns_404(client):
    response = client.get("/api/sensors/99999")
    
    assert response.status_code == 404
    

def test_delete_sensor(client):
    response = client.post(
        "/api/sensors",
        json={
            "name": "Delete-Me",
            "temperature": 45,
            "status": "offline",
        },
    )
    
    sensor_id = response.json()["id"]
    
    delete_response = client.delete(f"/api/sensors/{sensor_id}")
    assert delete_response.status_code == 204
    
    assert client.get(f"/api/sensors/{sensor_id}").status_code == 404
    