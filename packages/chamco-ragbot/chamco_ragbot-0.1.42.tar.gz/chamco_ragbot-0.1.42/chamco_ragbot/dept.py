import logging

# from chamco_ragbot.utils import parse_file_url, sanitize_folder_name
from chamco_ragbot.acl import update_file_metadata



def process_departments(depts_dict, dept_name, file_name, BLOB_CONTAINER_NAME):
    # folder_full, folder_name, file_name = parse_file_url(file_url)

    if depts_dict is not None:
        department_group_id = depts_dict.get(dept_name)
        if department_group_id is not None:
            update_file_metadata(file_name, dept_name, department_group_id, BLOB_CONTAINER_NAME)
            
            
            logging.info("[Ok] RAG update completed")
        else:
            logging.error(f"Department group ID not found for {dept_name}.")
    else:
        logging.error("Error: Departments dictionary not populated.")




def process_departments_new(dept_name, file_name, BLOB_CONTAINER_NAME):
    # folder_full, folder_name, file_name = parse_file_url(file_url)

    # if dept_name is not None:
    #     department_group_id = depts_dict.get(dept_name)
    #     if department_group_id is not None:
    update_file_metadata(file_name, dept_name, BLOB_CONTAINER_NAME)
            
            
    #         logging.info("[Ok] RAG update completed")
    #     else:
    #         logging.error(f"Department group ID not found for {dept_name}.")
    # else:
    #     logging.error("Error: Departments dictionary not populated.")
