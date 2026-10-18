from contextlib import closing
import main_app as application


def test_api_data_is_persisted_in_database(client):
    # Arrange: create a sensor through the API.
    payload = {
        "name": "Compressor-01",
        "temperature": 88.4,
        "status": "online",
}
    
    response = client.post("/api/sensors", json=payload)
    assert response.status_code == 201
    sensor_id = response.json()["id"]
    
    # Act: query the database directly.
    with closing(application.connect_db()) as db:
        row = db.execute(
            "SELECT * FROM sensors WHERE id = ?",
            (sensor_id,)
        ).fetchone()
        
    # Assert: compare API input with stored database values.
    assert row is not None
    assert row["name"] == "Compressor-01"
    assert row["temperature"] == 88.4
    assert row["status"] == "online"
    
    
def test_update_is_persisted(client):
    created = client.post(
        "/api/sensors",
        json={
            "name": "Pump-10",
            "temperature": 50,
            "status": "offline",
        },
    ).json()
    
    sensor_id = created["id"]
    
    response = client.patch(f"/api/sensors/{sensor_id}", json={
        "name": "Pump-10",
        "temperature": 75,
        "status": "online",
    })
    
    assert response.status_code == 200
    
    with closing(application.connect_db()) as db:
        row = db.execute(
            "SELECT * FROM sensors WHERE id = ?",
            (sensor_id,)
        ).fetchone()
    
    assert row["temperature"] == 75
    assert row["status"] == "online" 