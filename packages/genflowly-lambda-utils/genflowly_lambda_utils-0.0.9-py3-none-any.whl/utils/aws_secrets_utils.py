import boto3
from botocore.exceptions import ClientError
import base64
import logging

from utils.contants import AWS_DEFAULT_REGION

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_secret(secret_name: str) -> dict:

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=AWS_DEFAULT_REGION
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        logger.error("Couldn't retrieve the secret: %s", e)
        return {"status": 500, "response": e}
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        return {"status": 200, "response": secret}
