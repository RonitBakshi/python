import socketio
import time

# Replace with your server's address and port
SERVER_URL = 'http://localhost:3001'
NAMESPACE = '/chat/66828afc93039b75dad55693'

# Create a Socket.IO client instance
sio = socketio.Client(engineio_logger=False)

emit_time = None
first_response_time = None
last_response_time = None
first_token = True

@sio.event
def chat(response):
    global first_response_time, last_response_time, first_token

    if response['action'] == 'getMessageResponse':

        if first_token:
            first_response_time = time.time()
            first_token = False

        if 'message' in  response:
            if response['message'] == 'Message sent successfully':
                last_response_time = time.time()
                # print(response) 

                print(f"First token time: {first_response_time - emit_time}")
                print(f"Completely token time: {last_response_time - emit_time}")

@sio.event
def connect():
    print('Connected to the server')

@sio.event
def disconnect():
    print('Disconnected from server')

if __name__ == '__main__':
    try:
        headers = {
            'Authorization': 'Bearer your_jwt_token',
            'Custom-Header': 'custom_value'
            
        }

        sio.connect(SERVER_URL + NAMESPACE, headers=headers)
        
        request_data = {
            'action': 'getMessageResponse',
            'body': { 'content': 'Hello, how are you?' },
            'params': { 'characterId': '66828afc93039b75dad55693' },
            'user': {
                'exp': 1720515665,
                'iat': 1720514765,
                'auth_time': 1719989802,
                'jti': 'd8b3fe3a-544d-411c-ac97-6cd02b5a7495',
                'iss': 'https://devauth.chatreal.ai/realms/chatreal',
                'aud': 'account',
                'sub': '4b0f611b-8c50-43c6-8e68-a8166e2b8aa4',
                'typ': 'Bearer',
                'azp': 'chatreal-web',
                'session_state': 'f520b052-74de-4b58-b21c-41781e0b3d7e',
                'acr': '0',
                'allowed-origins': [ '*', 'https://chatreal.ai', 'http://localhost:3000' ],
                'realm_access': { 'roles': ['default-roles-chatreal', 'offline_access', 'uma_authorization'] },
                'resource_access': { 'account': {} },
                'scope': 'openid email profile',
                'sid': 'f520b052-74de-4b58-b21c-41781e0b3d7e',
                'email_verified': True,
                'preferred_username': 'ronit.4waytechnologies@gmail.com',
                'email': 'ronit.4waytechnologies@gmail.com',
                'kid': '4b0f611b-8c50-43c6-8e68-a8166e2b8aa4',
                'roles': ['default-roles-chatreal', 'offline_access', 'uma_authorization']
            },
            'socket': None,
            'io': None
        }

        emit_time = time.time()
        sio.emit('chat', request_data)
        
        sio.wait()
    except socketio.exceptions.ConnectionError as e:
        print(f'Connection error: {e}')
