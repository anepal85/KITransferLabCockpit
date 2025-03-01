# Define the URL where Label Studio is accessible and the API key for your user account


LABEL_STUDIO_URL = 'http://localhost:8080'

# Import the SDK and the client module
from label_studio_sdk import Client
from label_studio_base_url import * 



# Connect to the Label Studio API and check the connection
ls = Client(url=LABEL_STUDIO_URL, api_key=token)
ls.check_connection()
headers = {"Authorization": f"Token {token}"}

session = ls.get_session()
session.headers.update(headers)

new_url = ls.get_url('api/projects/13')

response = session.request(
        'GET',
        new_url,
        headers=headers
    )
print(response.json()['label_config'])