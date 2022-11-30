from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
from distutils.spawn import find_executable
from distutils import sysconfig, log
import setuptools
import setuptools.command.build_py
import setuptools.command.develop
import setuptools.command.build_ext

from collections import namedtuple
from contextlib import contextmanager
import glob
import shlex
import subprocess
import sys
import shutil
import platform
import multiprocessing

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
TOP_DIR = os.path.realpath(os.path.dirname(__file__))
TOP_DIR = os.path.split(TOP_DIR)[0]

PACKAGE_NAME = os.getenv("PACKAGE_NAME", "faceapi")
wheel_name = "faceapi-python"

with open(os.path.join(TOP_DIR, "python", "requirements.txt")) as fin:
    REQUIRED_PACKAGES = fin.read()

setup_configs = dict()

setup_configs["BUILD_WITH_GPU"] = os.getenv("BUILD_WITH_GPU", "OFF")
setup_configs["CUDA_DIR"] = os.getenv("CUDA_DIR", "")
setup_configs["PY_LIBRARY_NAME"] = "py" + PACKAGE_NAME

if setup_configs["BUILD_WITH_GPU"] == "ON":
    wheel_name = "faceapi-gpu-python"

if os.getenv("CMAKE_CXX_COMPILER", None) is not None:
    setup_configs["CMAKE_CXX_COMPILER"] = os.getenv("CMAKE_CXX_COMPILER")

SRC_DIR = os.path.join(TOP_DIR, PACKAGE_NAME)
CMAKE_BUILD_DIR = os.path.join(TOP_DIR, 'python', '.setuptools-cmake-build')

CMAKE = find_executable('cmake3') or find_executable('cmake')
MAKE = find_executable('make')

setup_requires = []
extras_require = {}

################################################################################
# Global variables for controlling the build variant
################################################################################

# Default value is set to TRUE\1 to keep the settings same as the current ones.
# However going forward the recomemded way to is to set this to False\0
USE_MSVC_STATIC_RUNTIME = bool(
    os.getenv('USE_MSVC_STATIC_RUNTIME', '1') == '1')
################################################################################
# Version
################################################################################

try:
    git_version = subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'], cwd=TOP_DIR).decode('ascii').strip()
except (OSError, subprocess.CalledProcessError):
    git_version = None
with open(os.path.join(TOP_DIR, 'VERSION_NUMBER')) as version_file:
    VersionInfo = namedtuple('VersionInfo', ['version', 'git_version'])(
        version=version_file.read().strip(), git_version=git_version)

################################################################################
# Pre Check
################################################################################

assert CMAKE, 'Could not find "cmake" executable!'


################################################################################
# Utilities
################################################################################


@contextmanager
def cd(path):
    if not os.path.isabs(path):
        raise RuntimeError('Can only cd to absolute path, got: {}'.format(
            path))
    orig_path = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(orig_path)


################################################################################
# Customized commands
################################################################################


def copy_files(dir_name, dst_directory):
    for result in os.listdir(dir_name):
        result_ = os.path.join(dir_name, result)
        if os.path.isdir(result_):
            copy_files(result_, dst_directory)
        else:
            new_file = os.path.join(dst_directory, result)
            if result_.split(".")[-1] in ["dll", "pyd", "so", "dylib"] and not result_.__contains__("tennis_"):
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

    for f in all_files:
        if f.split(".")[-1] in ["dll", "pyd", "so", "dylib"]:
            package_data.append(
                os.path.relpath(f, os.path.join(parent_dir, "faceapi")))
    return package_data


class cmake_build(setuptools.Command):
    """
    Compiles everything when `python setupmnm.py build` is run using cmake.
    Custom args can be passed to cmake by specifying the `CMAKE_ARGS`
    environment variable.
    The number of CPUs used by `make` can be specified by passing `-j<ncpus>`
    to `setup.py build`.  By default all CPUs are used.
    """
    user_options = [(str('jobs='), str('j'),
                     str('Specifies the number of jobs to use with make'))]

    built = False

    def initialize_options(self):
        self.jobs = None

    def finalize_options(self):
        if sys.version_info[0] >= 3:
            self.set_undefined_options('build', ('parallel', 'jobs'))
        if self.jobs is None and os.getenv("MAX_JOBS") is not None:
            self.jobs = os.getenv("MAX_JOBS")
        self.jobs = multiprocessing.cpu_count() if self.jobs is None else int(
            self.jobs)

    def run(self):
        if cmake_build.built:
            return
        cmake_build.built = True
        if not os.path.exists(CMAKE_BUILD_DIR):
            os.makedirs(CMAKE_BUILD_DIR)

        with cd(CMAKE_BUILD_DIR):
            build_type = 'Release'
            # configure
            cmake_args = [CMAKE, '-DPYTHON_INCLUDE_DIR={}'.format(sysconfig.get_python_inc()),
                          '-DPYTHON_EXECUTABLE={}'.format(sys.executable), '-DBUILD_PYTHON=ON',
                          '-DCMAKE_BUILD_TYPE=%s' % build_type]
            for k, v in setup_configs.items():
                cmake_args.append("-D{}={}".format(k, v))
            if platform.system().lower() == "windows":
                cmake_args.extend([
                    # we need to link with libpython on windows, so
                    # passing python version to window in order to
                    # find python in cmake
                    '-DPY_VERSION={}'.format('{0}.{1}'.format(* \
                                                                  sys.version_info[:2])),
                ])
                if platform.architecture()[0] == '64bit':
                    cmake_args.extend(['-A', 'x64', '-T', 'host=x64'])
                else:
                    cmake_args.extend(['-A', 'Win32', '-T', 'host=x86'])
            if 'CMAKE_ARGS' in os.environ:
                extra_cmake_args = shlex.split(os.environ['CMAKE_ARGS'])
                # prevent crossfire with downstream scripts
                del os.environ['CMAKE_ARGS']
                log.info('Extra cmake args: {}'.format(extra_cmake_args))
                cmake_args.extend(extra_cmake_args)
            print("Cmake Options:", cmake_args)
            cmake_args.append(TOP_DIR)
            subprocess.check_call(cmake_args)

            build_args = [CMAKE, '--build', os.curdir]
            build_args.extend((['--target', setup_configs["PY_LIBRARY_NAME"]]))
            if platform.system().lower() == "windows":
                build_args.extend(['--config', build_type])
                build_args.extend(['--', '/maxcpucount:{}'.format(self.jobs)])
            else:
                build_args.extend(['--', '-j', str(self.jobs)])

            subprocess.check_call(build_args)


class build_py(setuptools.command.build_py.build_py):
    def run(self):
        self.run_command('cmake_build')

        generated_python_files = \
            glob.glob(os.path.join(CMAKE_BUILD_DIR, PACKAGE_NAME, '*.py')) + \
            glob.glob(os.path.join(CMAKE_BUILD_DIR, PACKAGE_NAME, '*.pyi'))
        for src in generated_python_files:
            dst = os.path.join(TOP_DIR, os.path.relpath(src, CMAKE_BUILD_DIR))
            self.copy_file(src, dst)

        return setuptools.command.build_py.build_py.run(self)


class develop(setuptools.command.develop.develop):
    def run(self):
        self.run_command('build_py')
        setuptools.command.develop.develop.run(self)


class build_ext(setuptools.command.build_ext.build_ext):
    def run(self):
        self.run_command('cmake_build')
        setuptools.command.build_ext.build_ext.run(self)

    def build_extensions(self):
        for ext in self.extensions:
            fullname = self.get_ext_fullname(ext.name)
            filename = os.path.basename(self.get_ext_filename(fullname))
            lib_path = os.path.join(CMAKE_BUILD_DIR, "lib")
            if sys.platform == 'win32':
                lib_path = os.path.join(lib_path, "win")
            elif sys.platform == 'linux':
                lib_path = os.path.join(lib_path, "linux")
            elif sys.platform == 'darwin':
                lib_path = os.path.join(lib_path, "mac")
            if sys.platform == 'win32':
                debug_lib_dir = os.path.join(lib_path, "Debug")
                release_lib_dir = os.path.join(lib_path, "Release")
                if os.path.exists(debug_lib_dir):
                    lib_path = debug_lib_dir
                elif os.path.exists(release_lib_dir):
                    lib_path = release_lib_dir
            src = os.path.join(lib_path, filename)
            dst = os.path.join(
                os.path.realpath(self.build_lib), PACKAGE_NAME, "libs", filename)
            self.copy_file(src, dst)


cmdclass = {
    'cmake_build': cmake_build,
    'build_py': build_py,
    'develop': develop,
    'build_ext': build_ext,
}

################################################################################
# Extensions
################################################################################


packages = setuptools.find_packages(exclude=['scripts'])
package_data = dict()
package_data[PACKAGE_NAME] = []

if sys.argv[1] == "install" or sys.argv[1] == "bdist_wheel":

    if not os.path.exists(
            os.path.join(TOP_DIR, "python", "faceapi", "libs")):
        print(
            "Didn't detect path: faceapi/libs exist, please execute `python setup.py build` first"
        )
        sys.exit(0)
    all_lib_data = process_libraries(CMAKE_BUILD_DIR)
    package_data[PACKAGE_NAME].extend(all_lib_data)
    setuptools.setup(
        name=wheel_name,
        version=VersionInfo.version,
        description="Deploy Kit Tool For Deeplearning models.",
        packages=packages,
        package_data=package_data,
        include_package_data=True,
        setup_requires=setup_requires,
        extras_require=extras_require,
        author='',
        author_email='',
        url='',
        install_requires=REQUIRED_PACKAGES,
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT",
            "Operating System :: OS Independent",
        ],
        license='MIT')
else:
    setuptools.setup(
        name=wheel_name,
        version=VersionInfo.version,
        description="face recognition models.",
        cmdclass=cmdclass,
        packages=packages,
        package_data=package_data,
        include_package_data=False,
        setup_requires=setup_requires,
        extras_require=extras_require,
        author='',
        author_email='',
        url='',
        install_requires=REQUIRED_PACKAGES,
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT",
            "Operating System :: OS Independent",
        ],
        license='MIT')
