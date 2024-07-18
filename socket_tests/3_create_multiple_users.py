import requests

def create_multiple_users(total_users,file_path):

    with open(file_path,'w') as file:

        for i in range(total_users):
            email = f"FakeEmail-{i}@gmail.com"
            name = f"Fake Name {i}"
            kid = f"FakeKid{i}"

            create_single_user(email,name,kid)

            file.write(f"EMAIL: {email} | KID: {kid} | NAME: {name}\n")


def create_single_user(email,name,kid):
    url = "http://localhost:3001/api/user/create"

    payload = {
        'user': {
            'kid':kid,
            'name': name,
            'email': email
        },
        'name': name,
        'gender': 'Male'
    }

    try:
        response = requests.post(url=url,json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.content}")
    except Exception as err:
        print(f"An error occurred: {err}")
    else:
        print("Success!")
        print(f"Response: {response.json()}")


if __name__ == '__main__':
    total_users = 50
    file_path = "socket_tests/user_data.txt"

    create_multiple_users(total_users,file_path)