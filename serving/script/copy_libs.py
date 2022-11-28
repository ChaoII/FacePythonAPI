import shutil
import os

dst_directory = "../lib"
if not os.path.exists(dst_directory):
    os.mkdir(dst_directory)


def get_files(dir_name):
    for result in os.listdir(dir_name):
        result_ = os.path.join(dir_name, result)
        if os.path.isdir(result_):
            get_files(result_)
        else:
            new_file = os.path.join(dst_directory, result)
            if result_.split(".")[-1] in ["dll", "so", "dylib"] and not result_.__contains__("tennis_"):
                shutil.copy(result_, new_file)


get_files("../../build/lib")
