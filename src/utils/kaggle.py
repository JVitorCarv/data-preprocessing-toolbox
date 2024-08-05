import os
import kaggle
import zipfile

os.makedirs("data", exist_ok=True)

competition_dataset = "rsna-pneumonia-detection-challenge"
regular_dataset = "paultimothymooney/chest-xray-pneumonia"


def unzip_file(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
    os.remove(zip_path)


def download_and_unzip_dataset(dataset, is_competition=False):
    try:
        print(f"Downloading dataset {dataset}...")
        if is_competition:
            kaggle.api.competition_download_files(dataset, path="./data")
            zip_file = f"./data/{dataset}.zip"
        else:
            kaggle.api.dataset_download_files(dataset, path="./data")
            zip_file = f"./data/{dataset.split('/')[-1]}.zip"

        unzip_file(zip_file, "./data")

        print(
            f"Dataset {dataset} downloaded and unzipped in data/ folder successfully."
        )
    except kaggle.rest.ApiException as e:
        print(f"Failed to download dataset {dataset}: {e}")
    except FileNotFoundError as e:
        print(f"File not found error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


download_and_unzip_dataset(competition_dataset, is_competition=True)
download_and_unzip_dataset(regular_dataset)

print("All datasets downloaded and unzipped in the data/ folder successfully.")
