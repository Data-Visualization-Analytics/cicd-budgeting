import subprocess

class FetchDataset:
    def __init__(self,
                 endpoint_url = "http://localhost:9000",
                 source_file = "Budgeting sheet.xlsx",
                 target_file = "downloads/Budgeting sheet.xlsx"
                 ):
        self.endpoint_url = endpoint_url
        self.source_file = source_file
        self.target_file = target_file
        self.aws_cmd = f"aws --endpoint-url {self.endpoint_url} s3 cp '{self.source_file}' '{self.target_file}'"

    def download(self):
        subprocess.run(self.aws_cmd, shell=True, check=True)