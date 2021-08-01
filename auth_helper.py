from msal import authority
import yaml
import msal
import logging
import requests
import json
config = json.load(open('./config.json','r'))
endpoint="https://graph.microsoft.com/v1.0/users"
def get_msal_app(cache=None):
  # Initialize the MSAL confidential client
    auth_app = msal.ConfidentialClientApplication(
    config['client_id'],
    authority=config['authority'],
    client_credential=config['client_secret'])
    return auth_app

# Method to generate a sign-in flow
def get_sign_in():
    auth_app = get_msal_app()
    result=auth_app.acquire_token_silent(config['scopes'],account=None)
    if not result:
        logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
        result = auth_app.acquire_token_for_client(scopes=config["scopes"])
    
    if "access_token" in result:
        # Calling graph using the access token
        graph_data = requests.get(  # Use token to call downstream service
            endpoint,
            headers={'Authorization': 'Bearer ' + result['access_token']}, ).json()
        userPrincipalName=graph_data["value"][0]["userPrincipalName"]
        print("userPrincipalName:"+userPrincipalName)
        
        email_data = requests.get(
            endpoint +"/"+ userPrincipalName+"/messages",
            headers={'Authorization': 'Bearer ' + result['access_token']}).json()

        print("Graph API call result: ")
        print(json.dumps(email_data, indent=2))
    else:
        print(result.get("error"))
        print(result.get("error_description"))
        print(result.get("correlation_id"))  # You may need this when reporting a bug

get_sign_in()