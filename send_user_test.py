
import requests

url = "http://localhost:8000/user"

payload = {
    "email": "test@example.com",
    "username": "testuser",
    "hashed_password": "your_hashed_password_here"
}

response = requests.post(url, json=payload)

print(response.status_code)
print(response.json())
