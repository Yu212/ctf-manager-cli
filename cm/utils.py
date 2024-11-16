import os
import shutil
from urllib.parse import urlparse


def set_cd_path(ctx, path):
    out_cd_path = ctx.ensure_object(dict)["out_cd_path"]
    if out_cd_path:
        with open(out_cd_path, "w") as f:
            f.write(path)

def copy_files(source_directory, dest):
    for file_name in os.listdir(source_directory):
        source_file_path = os.path.join(source_directory, file_name)
        dest_file_path = os.path.join(dest, file_name)
        copy_file_or_directory(source_file_path, dest_file_path)

def copy_file_or_directory(src, dest):
    if os.path.isdir(src):
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)

def is_url(s):
    try:
        result = urlparse(s)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
