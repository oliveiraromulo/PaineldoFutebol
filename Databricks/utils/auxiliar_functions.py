import os
import json
from databricks.sdk import WorkspaceClient

# Define volume, folder, and file details.
# catalog = 'footballdb'
# schema = 'default'
# volume = 'jsonfiles'
# volume_folder = 'fixtures'

#volume_path = f"/Volumes/{catalog}/{schema}/{volume}" # /Volumes/main/default/my-volume
#volume_folder_path = f"{volume_path}/{volume_folder}/{volume_file}" # /Volumes/main/default/my-volume/my-folder
def init_databricks_credentials():
    """
    Initializes the Databricks WorkspaceClient using credentials from a JSON configuration file.
    """
    try:
        #config_path = '/opt/airflow/dags/soccer_analytics/configDatabricks.json'
        #config_path = '/home/romulo/Documents/Git/PaineldoFutebol/Docs/Airflow/dags/soccer_analytics/configDatabricks.json'
        config_path = '/Workspace/Users/spcoromulo@gmail.com/PaineldoFutebol/Databricks/configDatabricks.json'
        with open(config_path) as file:
            args = json.load(file)

        w = WorkspaceClient(host=args['host'], token=args['token'])
        return w
    except Exception as e:
        print(f"Error initializing WorkspaceClient: {e}")
        return None
    
def upload_file_to_volume(local_file_path: str, catalog: str, volume: str, folder: str, filename: str):
    """
    Uploads a file to a Databricks volume.

    Args:
        local_file_path (str): The local path of the file to upload.
        volume_folder_path (str): The destination path in the Databricks volume.
    """

    volume_folder_path = f"/Volumes/{catalog}/default/{volume}/{folder}/{filename}" #
    try:        
        w = init_databricks_credentials()
        print(f"Sending file to {volume_folder_path}")
        with open(local_file_path, "rb") as f:
            w.files.upload(volume_folder_path, f.read(), overwrite=True)
        print(f"File uploaded successfully to {volume_folder_path}")
    except Exception as e:
        #print(f"Error uploading file: {e}")
        raise Exception(f"Error uploading file: {e}")


def get_api_credentials(env: str) -> dict:
    """
    Retrieves API credentials from a JSON configuration file based on the specified environment.

    Args:
        env (str): The environment for which to retrieve credentials (e.g., 'dev', 'prod').
    """

    if env in ["prd"]:
        #config_path = '/opt/airflow/dags/soccer_analytics/config.json'
        config_path = '/Workspace/Users/spcoromulo@gmail.com/PaineldoFutebol/Databricks/config.json'
    elif env in ["dev"]:
        config_path = '/home/romulo/Documents/Git/PaineldoFutebol/Serie B 2021/Codigos/config.json'

    file = open(config_path)
    args = json.load(file)
    file.close()

    return args