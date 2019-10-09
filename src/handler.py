import os
import json
import boto3
import http.client, urllib.parse
from src.response import return_success, return_failure
   
AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
TABLE_NAME = os.environ.get('TABLE_NAME')

conn = http.client.HTTPSConnection(AUTH0_DOMAIN)

table = boto3.resource('dynamodb', region_name="us-east-1").Table(TABLE_NAME)

def index(event: dict, context):
    
    param = event.get('queryStringParameters', {})
    if param:
        AUTHORIZATION_CODE = param['code']
        STATE = param['state']

        token = get_token(AUTHORIZATION_CODE)
        user_profile = get_user_profile(token)
        
        pk = 'user_profile'
        sk = user_profile['sub']

        entity = {'pk': pk, 'sk': sk, **user_profile}

        print(entity)
        resp = table.get_item(
            Key={
                'pk': entity.get('pk'),
                'sk': entity.get('sk')
            }
        )
      
        item = resp.get('Item')

        if item is None:
            """
            store user_info to UserTable
            """
            try:
                results = table.put_item(
                    Item=entity
                )
                return return_success({"status": True, "data": user_profile})
                
            except Exception as e:
                print(str(e))
                return return_failure({"status": False, "msg": str(e)})
        else:
            """
            retrieve user_info from UserTable
            """
            results = item
            return return_success(results)
        
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
    if token is None:
        return return_failure({"fail_msg": "Invalid token!!!"})

    id_token = token.get('id_token', None)
    payload = {
        'id_token': id_token
    }
    headers = {
        'Authorization': 'Bearer {}'.format(token.get('access_token')),
        'Content-Type': 'application/json'
    }
    body = json.dumps(payload)
    conn.request("GET", "/userinfo", body, headers)
    res = conn.getresponse()
    data = res.read()
    results = json.loads(data.decode("utf-8"))
    return results
