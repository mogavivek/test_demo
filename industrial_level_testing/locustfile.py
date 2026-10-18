from locust import HttpUser, task, between

class SensorUser(HttpUser):
    # Each simulated user waits 1–2 seconds between tasks.
    wait_time = between(1, 2)
    
    @task(3)
    def read_sensors(self):
        with self.client.get(
            "/api/sensors",
            name="GET sensor list",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure("Could not retrieve sensors")
                return
            
            if not isinstance(response.json(), list):
                response.failure("Expected a JSON list")
        
    
    @task(1)
    def check_health(self):
        self.client.get("/health", name="GET health")   