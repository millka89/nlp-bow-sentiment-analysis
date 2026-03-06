import requests
import zipfile
import io
import os
from dotenv import load_dotenv

load_dotenv()

KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME")
KAGGLE_KEY = os.getenv("KAGGLE_KEY")

DATA_DIR = "./data"
DATASET_URL = "https://www.kaggle.com/api/v1/datasets/download/snap/amazon-fine-food-reviews"


def create_data_dir():
    """Create folder data/ if not exists"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Folder created:{DATA_DIR}")
    else:
        print(f"Folder {DATA_DIR} already exists")

def download_dataset():
    """Download and unzip Amazon reviews dataset from Kaggle API"""
    if not KAGGLE_USERNAME or not KAGGLE_KEY:
        raise ValueError("Missing KAGGLE_USERNAME or KAGGLE_KEY in .env file!")
    
    print("Downloading dataset from Kaggle...")
    response = requests.get(
        DATASET_URL,
        auth=(KAGGLE_USERNAME, KAGGLE_KEY),
        stream=True
    )

    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(DATA_DIR)
        print(f"Done! Files saved in {DATA_DIR}:")
        for f in os.listdir(DATA_DIR):
            print(f"   - {f}")
    else:
        raise ConnectionError(f"Error {response.status_code}: {response.text}")
    
if __name__ == "__main__":
    create_data_dir()
    download_dataset()
