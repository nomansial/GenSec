import requests

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
    response.raise_for_status()  # Raise an error for non-2xx responses
    #print("idToken:", response.json().get("idToken"))
    return response.json().get("idToken")
