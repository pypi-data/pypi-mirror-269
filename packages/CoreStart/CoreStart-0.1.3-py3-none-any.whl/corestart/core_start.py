# src/corestart/core_start.py
import subprocess
import pkg_resources

def run():
    script_path = pkg_resources.resource_filename('corestart', 'core_start.sh')
    subprocess.call(f'/bin/bash {script_path}', shell=True)

