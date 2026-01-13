import os
import subprocess

class UploadDataset:
    def __init__(self,
                 endpoint_url = "http://localhost:9000",
                 processed_file_path = "income.csv",
                 target_file = "s3://processed-dataset/income.csv"
                 ):
        self.endpoint_url = endpoint_url
        self.processed_file_path = os.path.abspath(processed_file_path)
        self.target_file = target_file
        self.aws_cmd = f"aws --endpoint-url {self.endpoint_url} s3 cp '{self.processed_file_path}' '{self.target_file}'"

    def upload_to_s3(self):
        subprocess.run(self.aws_cmd, shell=True, check=True)