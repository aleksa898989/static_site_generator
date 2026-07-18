import os
import shutil


def copy_static_to_public(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    copy_directory_contents(src, dst)


def copy_directory_contents(src, dst):
    for name in os.listdir(src):
        src_path = os.path.join(src, name)
        dst_path = os.path.join(dst, name)
        if os.path.isfile(src_path):
            print(f"Copying {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            os.mkdir(dst_path)
            copy_directory_contents(src_path, dst_path)
