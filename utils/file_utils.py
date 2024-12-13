"""
-- Created by Bikash Saud
-- Created on 2023-06-28
"""
import os
import uuid

from django.conf import settings


def get_media_file_path(parent_dir, file_ext, child_dir=None):
    """
    :param parent_dir: Directory after media where you want to save file
    :param file_ext: media_filename
    :param child_dir: Directory inside parent directory if needed
    :return: file absolute path, url, and file_name
    """
    try:
        root_path = settings.MEDIA_ROOT
        base_url = settings.SITE_HOST
        print(base_url, 99999999999)
        if child_dir:
            file_url = f"{base_url}/media/{parent_dir}/{child_dir}"
            file_dir = os.path.join(root_path, parent_dir, child_dir)
        else:
            file_url = f"{base_url}/media/{parent_dir}"
            file_dir = os.path.join(root_path, parent_dir)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir, exist_ok=True)
        print(file_dir)
        # file_name = get_file_name(file_ext)
        file_name = "yojana_export_data.xlsx"
        file_path = os.path.join(file_dir, file_name)
        file_url = f"{file_url}/{file_name}"
        return file_path, file_url, file_name
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None


def get_file_name(ext):
    return f"{str(uuid.uuid4()).replace('-', '')}.{ext}"
