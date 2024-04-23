import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from . import models
from django.contrib.auth import models as modelss
import jwt
import json


@csrf_exempt
def my_api_view(request):
    api_key = request.headers.get('api_key')

    payload = json.loads(request.body)
    print(payload)

    print(api_key)
    developer_account = models.DeveloperAccount.objects.filter(
        api_key=api_key, is_active=True).first()
    if developer_account:
        # API key is valid
        # Your API logic here

        '''payload = {

            "username": "stebo",
            "password": "Nyunyetic@1",
            "type": "transfer",
            "card_id": "+26662509074",
            "billing_amount": "10",
            "billing_currency": "LSL",
            "Token": "21qwqw"

        }
        '''

        api_client = MyAPIClient("http://localhost:8000", "Authorization")

        login_user = api_client.user_login("/login", payload)

        print(login_user)
        access_token = login_user['tokena']

        if access_token:
            token = access_token
            decoded_token = jwt.decode(
                token, options={"verify_signature": False})

            # Use the payload as needed
            print(decoded_token)
            # Create or retrieve the user based on the user_data
            user_id = {
                'id': decoded_token['user_id']
            }

            request.session['user'] = user_id
            send_money = api_client.pay_data("lebelo/", access_token, payload)

        print(send_money)
        print(request.session['user'])
        response = JsonResponse({'message': send_money['message']})
        return response

    else:
        # API key is invalid or inactive
        return JsonResponse({'message': 'Invalid API key'}, status=401)


@csrf_exempt
class MyAPIClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def get_data(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "api_key": f"Bearer {self.api_key}",

            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        return response.json()

    def post_data(self, endpoint, auth_key, data):
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {auth_key}",
            "api_key": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()

    def pay_data(self, endpoint, auth_key, data):
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {auth_key}",
            "api_key": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()

    def user_login(self, endpoint,  data):
        url = f"{self.base_url}/{endpoint}"
        headers = {

            "api_key": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()


# Example usagexaxasax
