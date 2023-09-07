import os
import requests
import base64
import argparse

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
parser.add_argument('-rp', '--repo_path')
parser.add_argument('-fp', '--folder_path')

args = parser.parse_args()
repo_path=args.repo_path
local_folder_path=args.folder_path

# Artifactory API URL
artifactory_url = "https://ubit-artifactory-ba.intel.com/artifactory"

# Artifactory repository path where you want to upload the folder
repository_path = f"psg-ipse-ip-mcdma-bs-ba-local/{repo_path}"

# Artifactory username and API key for authentication
username = "koppulac"
api_key = "AKCp8pQmFtCQWgCyg3p4mu85ofKAShyuKovdypaqYcEAMLy9xDCi9TNbezUEi5iVUXzwV1r3U"


# Function to upload a file to Artifactory
def upload_file(file_path,base_path):
    file_name = file_path.replace(base_path,"")
    print(file_name)
    target_url = f"{artifactory_url}/{repository_path}/{file_name}"

    # Encode credentials as Base64
    credentials = f"{username}:{api_key}"
    auth_header = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_header}"
    }

    with open(file_path, "rb") as file:
        response = requests.put(target_url, data=file, headers=headers)

    if response.status_code == 201:
        print(f"Uploaded {file_name} successfully")
    else:
        print(f"Failed to upload {file_name}. Status code: {response.status_code}")
        print(response.text)

# Function to upload a folder recursively
def upload_folder(folder_path):
    local_path=os.path.split(folder_path)[0]
    print(local_path)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            upload_file(file_path,local_path)

# Start the folder upload process
upload_folder(local_folder_path)
