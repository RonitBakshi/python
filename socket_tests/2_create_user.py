import requests
import json

def user_creation():
    url = "http://localhost:3001/api/user/create"

    payload = {
        'user': {
            'kid':'12345678910ftr4ftr4',
            'name': 'fake user name',
            'email': 'ThisIsNonbmadwfvdsvzadsvhkltARealEmail@gmail.com'
        },
        'name': 'Fake name',
        'gender': 'male'
    }

    try:
        response = requests.post(url=url,json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        print(response)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.content}")
    except Exception as err:
        print(f"An error occurred: {err}")
    else:
        print("Success!")
        print(f"Response: {response.json()}")

if __name__ == '__main__':
    user_creation()
