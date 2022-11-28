import os
import sys
import shutil
import subprocess
import platform


def copy_files(dir_name, dst_directory):
    for result in os.listdir(dir_name):
        result_ = os.path.join(dir_name, result)
        if os.path.isdir(result_):
            copy_files(result_, dst_directory)
        else:
            new_file = os.path.join(dst_directory, result)
            if result_.split(".")[-1] in ["dll", "pyd" "so", "dylib"] and not result_.__contains__("tennis_"):
                shutil.copy(result_, new_file)


def get_all_files(dirname):
    files = list()
    for root, dirs, filenames in os.walk(dirname):
        for f in filenames:
            fullname = os.path.join(root, f)
            files.append(fullname)
    return files


def process_libraries(current_dir):
    parent_dir = os.path.dirname(current_dir)
    dst_directory = os.path.join(parent_dir, "faceapi", "libs")
    if os.path.exists(dst_directory):
        shutil.rmtree(dst_directory)
        os.mkdir(dst_directory)
    if platform.system().lower() == "linux":
        current_dir = os.path.join(current_dir, "lib", "linux")
        copy_files(current_dir, dst_directory)
    elif platform.system().lower() == "darwin":
        current_dir = os.path.join(current_dir, "lib", "mac")
        copy_files(current_dir, dst_directory)
    elif platform.system().lower() == "windows":
        current_dir = os.path.join(current_dir, "lib", "win")
        copy_files(current_dir, dst_directory)
    all_files = get_all_files(os.path.join(parent_dir, "faceapi", "libs"))
    package_data = list()
    if platform.system().lower() == "windows":
        for f in all_files:
            if f.endswith(".pyd") or f.endswith("lib") or f.endswith("dll"):
                package_data.append(
                    os.path.relpath(f, os.path.join(parent_dir, "faceapi")))
        return package_data

    filters = [".vcxproj", ".png", ".java", ".h", ".cc", ".cpp", ".hpp"]
    for f in all_files:
        remain = True
        for flt in filters:
            if f.count(flt) > 0:
                remain = False
        filename = os.path.split(f)[-1]
        # Note(zhoushunjie): To add the trt libs below will increase the size of whl package by 450M.
        #        if filename in [
        #                "libnvinfer_plugin.so",
        #                "libnvinfer.so", "libnvonnxparser.so",
        #                "libnvparsers.so", "libnvcaffe_parser.so"
        #        ]:
        #            continue

        for lib_prefix in ["libnvinfer_plugin.so.8.",
                           "libnvinfer.so.8.", "libnvonnxparser.so.8.",
                           "libnvparsers.so.8.", "libnvcaffe_parser.so.8."]:
            if filename.startswith(lib_prefix):
                remain = False
                break

        if remain:
            package_data.append(
                os.path.relpath(f, os.path.join(parent_dir, "fastdeploy")))
    return package_data
