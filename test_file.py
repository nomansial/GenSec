import requests
import json

def get_firebase_id_token():
    url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyD08yxn7V_YAfkAY8mKDTYjfKV_qoPrdRQ"
    payload = {
        "email": "sampletenantb-1yak0_noman.sial9-customer-api@gmail.com",
        "password": "Test@123",
        "returnSecureToken": True,
        "tenantId": "SampleTenantB-1yak0"
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    id_token = response.json().get("idToken")

    return id_token

def call_genr3d_api():
    id_token = get_firebase_id_token()
    print("Firebase idToken:", id_token)
    url = "https://genr3d-api-user.generativesecurity.ai/environments"
    headers = {
        "Authorization": f"Bearer {id_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    # Print everything in the console
    print("Status Code:", response.status_code)
    print("Response Headers:", json.dumps(dict(response.headers), indent=4))
    try:
        print("Response JSON Body:", json.dumps(response.json(), indent=4))
    except ValueError:
        print("Response Text Body:", response.text)

    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    env_data = call_genr3d_api()
