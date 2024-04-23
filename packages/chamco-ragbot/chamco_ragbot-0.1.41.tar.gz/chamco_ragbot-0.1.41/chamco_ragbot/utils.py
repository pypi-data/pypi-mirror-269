


def parse_file_url(file_url):
    # Split the path into folder and file parts
    parts = file_url.split('/')
    
    # Extract the folder name (without file name)
    folder_full = '/'.join(parts[:-1])
    folder_name = parts[-2]
    
    # Extract the file name
    file_name = parts[-1]
    
    return folder_full, folder_name, file_name




import re
from urllib.parse import unquote

def sanitize_name(folder_name):
    # Convert to lowercase
    folder_name = folder_name.lower()
    
    # Remove non-alphanumeric characters and replace spaces with dashes
    folder_name = re.sub(r'[^a-z0-9\s-]', '', folder_name)
    
    # Replace multiple spaces with a single dash
    folder_name = re.sub(r'\s+', '-', folder_name)
    
    # Remove leading and trailing dashes
    folder_name = folder_name.strip('-')
    
    # Limit to 128 characters
    folder_name = folder_name[:128]
    
    return folder_name



def parse_sharepoint_link(item_link):
    # Define a regex pattern to match the SharePoint site URL
    site_pattern = r'https://[^/]+/sites/[^/]+'
    
    # Extract the site link using regex
    site_match = re.match(site_pattern, item_link)
    site_link = site_match.group() if site_match else None
    
    # Extract the file URL by removing the site link part
    file_url = item_link[len(site_link)+1:] if site_link else None
    
    # Unquote the file URL to remove %20 encoding
    file_url = unquote(file_url) if file_url else None
    
    # Split the file URL to get the folder name and file name
    parts = file_url.split('/')
    folder_name = parts[-2]
    full_folder_name = '/'.join(parts[:-1]) if len(parts) > 1 else None
    file_name = parts[-1] if len(parts) > 0 else None
    
    return folder_name, file_name, file_url, site_link, full_folder_name