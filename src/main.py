import sys

import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.addHandler(logging.StreamHandler(sys.stderr))

class S3Connector:
    def __init__(self,
                 url="http://localhost:9000",
                 profile_name = "minio"
                 ):
        self.profile_name = profile_name
        self.url = url
        self.session = boto3.Session(profile_name=self.profile_name)
        self.credentials = self.session.get_credentials()
        self.access_key = self.credentials.access_key
        self.secret_key = self.credentials.secret_key

        self.config = boto3.session.Config(signature_version='s3v4')

    def connect(self, aws_region='us-east-1'):
        # Use the credentials to create a client
        s3_client = boto3.client(
            's3',
            endpoint_url=self.url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=self.config,
            region_name=aws_region
        )
        return s3_client

def main():

    s3_client = S3Connector().connect()
    response = s3_client.list_objects_v2(Bucket='dataset')
    if 'Contents' in response:
        for obj in response['Contents']:
            print(obj['Key'])

if __name__ == "__main__":
    main()