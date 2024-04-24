from pathlib import Path
import datetime
from google.cloud import storage
from colorama import Fore


class Gcloud:
    def __init__(self, json_path: str):
        path = Path.home() / json_path
        self.client = storage.Client.from_service_account_json(str(path))
        self.status = f'{Fore.LIGHTBLUE_EX}🐻‍❄️ Gcloud:{Fore.RESET}'
        self.bucket_name = 'kevin-bi'
        self.bucket = self.client.bucket(self.bucket_name)

    def download_file(self, blob_path: str, file_path: Path):
        blob = self.bucket.blob(blob_path)
        blob.download_to_filename(file_path)
        print(f'{self.status} download {blob_path}')

    def upload_file(self, blob_path: str, file_path: Path):
        blob_path_full = f'{blob_path}/{file_path.name}'
        blob = self.bucket.blob(blob_path_full)
        blob.upload_from_filename(file_path)
        print(f'{self.status} upload {file_path.stem} to {blob_path}')
        return blob_path_full

    def generate_download_signed_url_v4(self, blob_file, minutes=15):
        blob = self.bucket.blob(blob_file)
        url = blob.generate_signed_url(
            version='v4',
            expiration=datetime.timedelta(minutes=minutes),
            method='GET',
        )
        print(f"{self.status} Presigned [{blob_file}] in {minutes} mins \n"
              f"Url: {url}"
        )
        return url


# path = Path.home() / 'PycharmProjects/retrieval/token_json/shopee-vn-product-team.json'
# file_path = Path.home() / 'PycharmProjects/retrieval/data/20240129/db.parq'
# blob_path = 'vm_matching_result'
# # Gcloud(str(path)).upload_file(blob_path, file_path)
# url = Gcloud(str(path)).generate_download_signed_url_v4('vm_matching_result/db.parq', minutes=60)

