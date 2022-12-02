import shutil
import os


def get_files(dir_name, dst_dir):
    for result in os.listdir(dir_name):
        result_ = os.path.join(dir_name, result)
        if os.path.isdir(result_):
            get_files(result_, dst_dir)
        else:
            new_file = os.path.join(dst_dir, result)
            if result_.split(".")[-1] in ["dll", "so", "dylib"] and not result_.__contains__("tennis_"):
                shutil.copy(result_, new_file)


def copy_files(src_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    get_files(src_dir, dst_dir)


if __name__ == "__main__":
    copy_files("../build/lib", "./lib")
