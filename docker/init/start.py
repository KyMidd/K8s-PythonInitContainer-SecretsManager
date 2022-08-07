#!/usr/bin/env python3

# Imports
import boto3
from botocore.exceptions import ClientError
import sys # Needed to take input from user for testing
import os # To create directories

# Search AWS for secrets matching secrets lists
def main():
    # Read list of secrets search strings as input values
    SECRETS_SEARCH_INPUT=sys.argv[1:]
    
    # Find all secret based on search string
    for secret_search_string in SECRETS_SEARCH_INPUT:
        print("We are searching for:", secret_search_string, "with wildcard matching")
        
        # Parse ARN into individual components
        parse_arn(secret_search_string)
        
        # Find region
        SecretRegion=parse_arn(secret_search_string)["region"]
        #print("Secret's region is:", SecretSearchRegion)
        
        # Find secret name for searching
        SecretSearchString=parse_arn(secret_search_string)["resource_name"]
        #print("Secret's search string is:", SecretSearchString)

        # Need to find all secrets that match inputs lists
        found_secrets = search_for_secrets(SecretSearchString, SecretRegion)

        # Create secrets directory
        directory="/tmp/init-secrets"

        try:
            print("Creating location for secrets")
            os.mkdir(directory)
        except OSError as error:
            #print(error)
            pass

        # Find secret values
        for secret_name in found_secrets:
            secretValue=get_secret_value(secret_name, SecretRegion)
            try:
                # Create a file if not exist and write to it
                fileName="/tmp/init-secrets/{}".format(secret_name)
                #print("Attempting to stage secret", secret_name, "at", fileName)
                file = open(fileName, "w")
                file.write(secretValue)
                print("Staged", secret_name, "at", fileName)
            except Exception as error:
                print(error)
                print("Error staging secrets, please investigate")
                print(os.listdir("/tmp/init-secrets"))

# Find all secrets that match string
def search_for_secrets(SecretSearchString, SecretSearchRegion):
    secret_search_string = SecretSearchString
    secret_search_region = SecretSearchRegion

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=secret_search_region,
    )

    try:
        list_secrets_response = client.list_secrets(
            MaxResults=100, #100 is max supported
            Filters=[
                {
                    'Key': 'name',
                    'Values': [
                        secret_search_string,
                    ]
                },
            ]
        )
    except ClientError as e:
            print("The requested secret search string returned no results: " + secret_search_string)
            print("The error is:", e)
    else:
        # Store all secrets in array:
        foundSecrets = []
        for secret_name in list_secrets_response["SecretList"]:
            #print("Found secrets:", secret_name["Name"])
            foundSecrets.append(secret_name["Name"])
        #print("The list of secrets is: ", foundSecrets)
        return(foundSecrets)

# Find all secrets that match string
def get_secret_value(SecretName, Region):
    secret_name = SecretName
    region_name = Region

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + secret_name + " was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", e)
        elif e.response['Error']['Code'] == 'DecryptionFailure':
            print("The requested secret can't be decrypted using the provided KMS key:", e)
        elif e.response['Error']['Code'] == 'InternalServiceError':
            print("An error occurred on service side:", e)
    else:
        # Secrets Manager decrypts the secret value using the associated KMS CMK
        # Depending on whether the secret was a string or binary, only one of these fields will be populated
        if 'SecretString' in get_secret_value_response:
            SecretValue = get_secret_value_response['SecretString']
            return(SecretValue)
        else:
            SecretValue = get_secret_value_response['SecretBinary']
            return(SecretValue)

# Parse ARN
def parse_arn(arn):
    # http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html
    elements = arn.split(':', 6)
    result = {
        'arn': elements[0],
        'partition': elements[1],
        'service': elements[2],
        'region': elements[3],
        'account': elements[4],
        'resource': elements[5],
        'resource_name': elements[6]
    }

    if '/' in result['resource']:
        result['resource_type'], result['resource'] = result['resource'].split('/',1)
    elif ':' in result['resource']:
        result['resource_type'], result['resource'] = result['resource'].split(':',1)
    return result

# Run
main()