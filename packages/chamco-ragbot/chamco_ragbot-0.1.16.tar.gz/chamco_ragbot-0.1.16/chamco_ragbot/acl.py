from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import DefaultAzureCredential
import os
import logging
import re

import asyncio

from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient

# Create a credential object. Used to authenticate requests
credential = ClientSecretCredential(
    tenant_id='803b8895-b793-4dc6-b891-6e822908030c',
    client_id='0253c6c2-a257-4bf0-af53-6c75f6d56527',
    client_secret='BnY8Q~~2uX5gKw1wHFvDsvb8sk1hyjLK3a6sJckv'
)
scopes = ['https://graph.microsoft.com/.default']

# Create an API client with the credentials and scopes.
client = GraphServiceClient(credentials=credential, scopes=scopes)


# from asgiref.sync import async_to_sync

# # dept_name = "GPTKB_HRTest"
# @async_to_sync
async def get_departments_group_ids():
    groups = await client.groups.get()
    depts_dict = {group.display_name: group.id for group in groups.value}
    return depts_dict





# import asyncio


# def get_departments_group_ids():
#     loop = asyncio.get_event_loop()
#     if loop.is_running():
#         groups = loop.run_until_complete(client.groups.get())
#     else:
#         new_loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(new_loop)
#         groups = new_loop.run_until_complete(client.groups.get())
#         new_loop.close()
#     depts_dict = {group.display_name: group.id for group in groups.value}
#     return depts_dict




storage_account_name = os.getenv('STORAGE_ACCOUNT_NAME', "datalakegen2chamco")
storage_account_key = os.getenv('STORAGE_ACCOUNT_KEY', "19jjtOaErMgLfp3TMpzNpk0DTqhzV3TdlIt4Ya2I0mqpuf/drmEVAIEGSMxbtbneb9fglsPiaMLJ+AStvbU1nw==")
# blob_container_name = os.getenv('BLOB_CONTAINER_NAME', "gptkbcontainer")

# set up the service client with the credentials from the environment variables
service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
    "https",
    storage_account_name
), credential=storage_account_key)


def get_clients(blob_container_name, dept_name, file_name):
    filesystem_client = service_client.get_file_system_client(blob_container_name)
    directory_client = filesystem_client.get_directory_client(dept_name)
    file_client = directory_client.get_file_client(file_name)
    return file_client, directory_client


def get_updated_file_metadata(file_metadata, department_group_id):

    updated_file_metadata = file_metadata.copy()

    if 'group_ids' in file_metadata:
        existing_group_ids = file_metadata['group_ids']
        if department_group_id not in existing_group_ids:
            updated_file_metadata['group_ids'] += f", {department_group_id}"
    else:
        updated_file_metadata['group_ids'] = str(department_group_id)
    
    return updated_file_metadata


def update_file_metadata(file_name, dept_name, blob_container_name):
    logging.info(f"[Ok]  Getting  directory client for {dept_name}")
    logging.info(f"[Ok]  Getting  file client for {file_name}")

    file_client, directory_client = get_clients(blob_container_name, dept_name, file_name)

    file_metadata = file_client.get_file_properties()['metadata']
    directory_info = directory_client.get_access_control()
    logging.info(f"[Ok]  Getting  directory_info {directory_info}")
    # file_info = file_client.get_access_control()
    acl = directory_info.get('acl')
    owner_group = directory_info.get('group')
    other_groups = re.findall(r'group:([\w-]+)', acl)

    logging.info(f"[Ok]  owner_group  {owner_group}")
    logging.info(f"[Ok]  other_groups {other_groups}")

    other_groups.append(owner_group) 
    group_ids = ', '.join(other_groups)

    updated_file_metadata = get_updated_file_metadata(file_metadata, group_ids)

    logging.info(f"[Ok]  current file metadata {file_metadata}")
    file_client.set_metadata(updated_file_metadata)
    logging.info(f"[Ok]  file metadata update with groups ids {updated_file_metadata}")



