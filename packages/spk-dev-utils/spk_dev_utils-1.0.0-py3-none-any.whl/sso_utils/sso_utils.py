import json
import os
import time
import boto3
import datetime

sso_start_url = None
sso_cache_folder = None
permission_set = None
account_id = None
region_name = None

def get_latest_access_token(sso_cache_folder=os.path.expanduser("~/.aws/sso/cache"), start_url='https://sparkmeter.awsapps.com/start#/'):
    """
    Extracts the most recent access token associated with the given start URL
    from the SSO cache files.
    """
    latest_token = None

    for filename in os.listdir(sso_cache_folder):
        filepath = os.path.join(sso_cache_folder, filename)
        if filename.endswith(".json"):
            with open(filepath, "r") as f:
                data = json.load(f)
                if data.get("startUrl") == start_url:
                    expires_at = data.get("expiresAt")
                    if expires_at:
                        # Convert expiresAt to a datetime object
                        expires_at_dt = datetime.datetime.strptime(
                            expires_at, "%Y-%m-%dT%H:%M:%SZ"
                        )

                        # Convert datetime object to Unix timestamp (float)
                        expires_at_timestamp = expires_at_dt.timestamp()

                        if time.time() < expires_at_timestamp:  # Check if not expired
                            latest_token = data.get("accessToken")
                            break

    return latest_token

def get_sso_account_id(access_token, region_name='us-east-1'):
    sso_client = boto3.client('sso', region_name=region_name)
    
    accounts = []
    next_token = None
    while True:
        try:
            if next_token:
                response = sso_client.list_accounts(
                    accessToken=access_token,
                    nextToken=next_token
                )
            else:
                response = sso_client.list_accounts(
                    accessToken=access_token
                )
            accounts.extend(response['accountList'])
            next_token = response.get('nextToken')
            if not next_token:
                break
        except Exception as ex:
            print(ex)
            return None  # Or handle the error more gracefully

    # Sort accounts alphabetically
    accounts.sort(key=lambda account: account['accountName'])

    print("Available accounts (sorted):")
    for index, account in enumerate(accounts):
        print(f"{index + 1}. {account['accountName']} ({account['accountId']})")
        
    while True:
        try:
            selected_index = int(input("Select an account by number: ")) - 1
            if 0 <= selected_index < len(accounts):
                account_id = accounts[selected_index]["accountId"]
                break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            
    return account_id

def get_sso_account_permission_set(access_token: str, account_id: str, region_name='us-east-1'):
    sso_client = boto3.client('sso', region_name=region_name)
    
    permission_sets = []
    next_token = None
    while True:
        try:
            if next_token:
                response = sso_client.list_account_roles(
                    accessToken=access_token, accountId=account_id, next_token=next_token
                )
            else:
                response = sso_client.list_account_roles(
                    accessToken=access_token, accountId=account_id
                )
            permission_sets.extend(response["roleList"])
            next_token = response.get('nextToken')
            if not next_token:
                break
        except Exception as ex:
            print(ex)
            return None  # Or handle the error more gracefully

    # Sort accounts alphabetically
    permission_sets.sort(key=lambda permission_sets: permission_sets['roleName'])

    print("Available Permission Sets:")
    for index, permission_set in enumerate(permission_sets):
        print(f"{index + 1}. {permission_set['roleName']}")
        
    while True:
        try:
            selected_index = int(input("Select a Permission Set by number: ")) - 1
            if 0 <= selected_index < len(permission_sets):
                permission_set = permission_sets[selected_index]["roleName"]
                break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            
    return permission_set
                
def get_boto3_session(
    access_token, account_id, permission_set=None, region_name="us-east-1"
) -> boto3.session.Session:  # Add optional region
    """
    Creates a Boto3 session using the access token, account ID, and permission set.
    Utilizes the SSO client's get_role_credentials method.
    """
    sso_client = boto3.client(
        "sso",
        region_name=region_name,
        aws_access_key_id="",
        aws_secret_access_key="",
        aws_session_token=access_token,
    )
    if not account_id:
        account_id = get_sso_account_id(access_token=access_token)
        
    if not permission_set:
        permission_set = get_sso_account_permission_set(
          access_token=access_token, account_id=account_id, region_name=region_name
        )

    response = sso_client.get_role_credentials(
        roleName=permission_set, accountId=account_id, accessToken=access_token
    )

    credentials = response["roleCredentials"]
    return boto3.Session(
        aws_access_key_id=credentials["accessKeyId"],
        aws_secret_access_key=credentials["secretAccessKey"],
        aws_session_token=credentials["sessionToken"],
    )


if __name__ == "__main__":
    access_token = get_latest_access_token(sso_cache_folder, sso_start_url)

    if access_token:
        if not account_id:
            account_id = get_sso_account_id(access_token)
          
        session = get_boto3_session(access_token, account_id, permission_set)
        print(f"Boto3 session established successfully to Account {account_id}.")
    else:
        print("No valid access token found. Please re-authenticate with AWS CLI.")