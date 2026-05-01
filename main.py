
import requests

class PracticeCode():
    def __init__(self):
        pass
    
    def get_weather(self, temp:int):
        if temp > 20:
            return "hot"
        else:
            return "cold"

    def add(self, a, b):
        return a + b

    def divide(self,a,b):
        if b == 0:
            raise ValueError("Cannot divide with zero")
        return a/b

class UserManager:
    def __init__(self):
        self.user = {}
    
    def add_user(self, username, email):
        if username in self.user:
            raise ValueError("User already exists")
        self.user[username] = email
        return True
    
    def get_user(self,username):
        return self.user.get(username)
    
class DataBase:
    def __init__(self):
        self.data = {}
    
    def add_data_user(self, user_id, name):
        if user_id == self.data:
            raise ValueError("User already exsists")
        self.data[user_id] = name
    
    def get_data_user(self, user_id):
        return self.data.get(user_id, None)
    
    def delete_data_user(self, user_id):
        if user_id in self.data:
            del self.data[user_id]
            
class CheckPrimeNumber:
    def __init__(self):
        pass
        
    def is_prime(self, n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) * 1):
            if n % i == 0:
                return False
        return True
    

class MockTest:
    def __init__(self):
        pass
    
    def get_weather_from_api(self, city):
        response = requests.get(f"https://api.weather.com/v1/{city}")
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError("Could not fetch weather data")