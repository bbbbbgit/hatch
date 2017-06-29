import json
import subprocess

from hatch.utils import NEED_SUBPROCESS_SHELL


def get_python_path():
    return subprocess.check_output(
        ['python', '-c', 'import sys;print(sys.executable)'], shell=NEED_SUBPROCESS_SHELL
    ).decode().strip()


def install_packages(packages):
    subprocess.call(['pip', 'install'] + packages, shell=NEED_SUBPROCESS_SHELL)


def get_package_version(package_name):
    output = subprocess.check_output(
        ['pip', 'list', '--format', 'json'], shell=NEED_SUBPROCESS_SHELL
    ).decode()
    packages = json.loads(output)
    for package in packages:
        if package['name'] == package_name:
            return package['version']
    return ''


def get_installed_packages(editable=True):
    output = subprocess.check_output(
        ['pip', 'list', '-e', '--format', 'json'], shell=NEED_SUBPROCESS_SHELL
    ).decode()
    editable_packages = set(package['name'] for package in json.loads(output))

    output = subprocess.check_output(
        ['pip', 'list', '--format', 'json'], shell=NEED_SUBPROCESS_SHELL
    ).decode()
    packages = [
        package['name'] for package in json.loads(output)
        if editable or package['name'] not in editable_packages
    ]

    return packages