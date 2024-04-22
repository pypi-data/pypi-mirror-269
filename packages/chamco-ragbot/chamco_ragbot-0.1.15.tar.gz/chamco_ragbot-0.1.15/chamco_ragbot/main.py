import os
import asyncio

from dotenv import load_dotenv
load_dotenv()

import sys
sys.path.append('/home/azureuser/projects/rag_chatbot/src/chamco_ragbot')


import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from chamco_ragbot.utils import parse_file_url, sanitize_name, parse_sharepoint_link

from chamco_ragbot.filetransfer import sharepoint_auth, download_sharepoint_file, upload_file_to_blob_container
from chamco_ragbot.acl import get_departments_group_ids, update_file_metadata
from chamco_ragbot.dept import process_departments

from chamco_ragbot.indexer import create_indexer, indexer_client

# from .filetransfer import sharepoint_auth, download_sharepoint_file, upload_file_to_blob_container
from chamco_ragbot.datasource import create_datasource
# from .chat import chat, get_context, get_response
from chamco_ragbot.index import create_index
from chamco_ragbot.indexer import create_indexer, indexer_client
from chamco_ragbot.skillset import create_skill_set

SHAREPOINT_SITE_URL = os.getenv("SHAREPOINT_SITE_URL")
SHAREPOINT_USERNAME = os.getenv("SHAREPOINT_USERNAME")
SHAREPOINT_PASSWORD = os.getenv("SHAREPOINT_PASSWORD")

BLOB_CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")



def update_blob_container(item_link):
    # folder_full, folder_name, file_name = parse_file_url(file_url)
    folder_name, file_name, file_url, site_link, full_folder_name = parse_sharepoint_link(item_link)
    dept_name = folder_name
    blob_name = os.path.join(folder_name, file_name)
    ctx = sharepoint_auth(site_link, SHAREPOINT_USERNAME, SHAREPOINT_PASSWORD)
    download_path = download_sharepoint_file(ctx, file_url)
    blob_name = upload_file_to_blob_container(download_path, blob_name, BLOB_CONNECTION_STRING, BLOB_CONTAINER_NAME)
        
    # Move subsequent code here
    update_file_metadata(file_name, dept_name, BLOB_CONTAINER_NAME)



def update_aisearch():

    folder_name = sanitize_name(BLOB_CONTAINER_NAME)
    logging.info(f"[Ok] {folder_name} folder name sanitized")
    logging.info(f"[Ok] {BLOB_CONTAINER_NAME} BLOB_CONTAINER_NAME")
    index = create_index(BLOB_CONTAINER_NAME)
    logging.info(f"[Ok] {index.name} index name")
    data_source = create_datasource(index_name=index.name)
    skillset = create_skill_set(index_name=index.name)
    # indexer_client.close()
    indexer_result = create_indexer(index.name, data_source, skillset.name)

    logging.info(f"[Ok] {indexer_result.name} indexer update completed")
    logging.info(f"[Ok] Resetting indexer {indexer_result.name}")
    indexer_client.reset_indexer(indexer_result.name)
    logging.info(f"[Ok] running indexer {indexer_result.name}")
    indexer_client.run_indexer(indexer_result.name)
    logging.info(f"[Ok] running indexer {indexer_result.name} completed")
    logging.info(f"[Ok] rag update completed")

