import sys
import boto3
import logging
from etl.download_dataset import FetchDataset
from etl.transform import Transformer
from etl.uploader import UploadDataset

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.addHandler(logging.StreamHandler(sys.stderr))

class S3Connector:
    def __init__(self,
                 url="http://host.docker.internal:9000"
                 ):
        self.url = url
        self.session = boto3.Session()
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
        return s3_client, self.url

def main():
    s3_client, url = S3Connector().connect()
    response = s3_client.list_objects_v2(Bucket='dataset')
    if 'Contents' in response:
        for obj in response['Contents']:
            print(obj['Key'])

    source_file = "s3://dataset/Budgeting sheet.xlsx"
    target_file = "downloads/Budgeting sheet.xlsx"
    step1 = FetchDataset(endpoint_url=url, source_file=source_file, target_file=target_file)
    step1.download()

    processed_file_path = 'downloads/income.csv'
    step2 = Transformer(downloaded_file_path=target_file, processed_file_path=processed_file_path)
    step2.mapper()

    target_file = "s3://processed-dataset/income.csv"
    step3 = UploadDataset(processed_file_path=processed_file_path, target_file=target_file)
    step3.upload_to_s3()

if __name__ == "__main__":
    main()