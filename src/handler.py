import os
import json
import boto3
import http.client, urllib.parse
from src.response import return_success, return_failure

client = boto3.client('dynamodb')
    
AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
TABLE_NAME = os.environ.get('TABLE_NAME')

conn = http.client.HTTPSConnection(AUTH0_DOMAIN)

def index(event: dict, context):
    
    param = event.get('queryStringParameters', [])
    if param:
        AUTHORIZATION_CODE = param['code']
        STATE = param['state']

        token = get_token(AUTHORIZATION_CODE)
        user_profile = get_user_profile(token)

        resp = client.get_item(
            TableName=TABLE_NAME,
            Key={
                'userId': { 'S': user_id }
            }
        )
        item = resp.get('Item')
        if not item:
            """
            store user_info to UserTable
            """
            pass    
        else:
            """
            retrieve user_info from UserTable
            """
            pass  

        return return_success(user_profile)
    else:
        fail_msg = "Oops, Invalid Request!!!"
        return return_failure(fail_msg)

def get_token(authorization_code):
    """
    Getting tokens
    """
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": authorization_code,
        "redirect_uri": AUTH0_CALLBACK_URL
    }
    headers = {
        'Content-Type': "application/x-www-form-urlencoded"
    }
    body = urllib.parse.urlencode(payload)
    conn.request("POST", "/oauth/token", body, headers)

    res = conn.getresponse()
    data = res.read()

    results = json.loads(data.decode("utf-8"))

    return results

def get_user_profile(token):
    """
    Getting User_Profile
    """
    payload = {
        'id_token': token['id_token']
    }
    headers = {
        'Authorization': 'Bearer {}'.format(token['access_token']),
        'Content-Type': 'application/json'
    }
    body = json.dumps(payload)
    conn.request("GET", "/userinfo", body, headers)
    res = conn.getresponse()
    data = res.read()
    results = json.loads(data.decode("utf-8"))
    return results