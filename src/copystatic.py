import os
import shutil

def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        to_path = os.path.join(dest_dir_path, filename)
        if os.path.isdir(from_path):
            copy_files_recursive(from_path, to_path)
        else:
            shutil.copy(from_path, to_path)