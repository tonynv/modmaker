#!/usr/bin/env python3
"""
Script to check version consistency across different files.
"""

import re
import os
import sys
import subprocess
from colorama import init, Fore, Style

# Initialize colorama
init()

def get_version_from_file(file_path, pattern):
    """Extract version from a file using the given pattern."""
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    match = re.search(pattern, content)
    if match:
        return match.group(1)
    return None

def get_pypi_version():
    """Get the latest version from PyPI."""
    try:
        result = subprocess.run(['pip', 'index', 'versions', 'modmaker'], 
                               capture_output=True, text=True, check=False)
        output = result.stdout
        match = re.search(r'modmaker \(([0-9.]+)\)', output)
        if match:
            return match.group(1)
        return None
    except Exception as e:
        print(f"Error getting PyPI version: {e}")
        return None

def main():
    """Main function to check version consistency."""
    files_to_check = [
        {
            'name': 'pyproject.toml',
            'file': 'pyproject.toml',
            'pattern': r'version = "([0-9.]+)"',
        },
        {
            'name': 'setup.cfg',
            'file': 'setup.cfg',
            'pattern': r'version = ([0-9.]+)',
        },
        {
            'name': '__init__.py',
            'file': '__init__.py',
            'pattern': r'__version__ = "([0-9.]+)"',
        },
        {
            'name': 'modmaker/__init__.py',
            'file': 'modmaker/__init__.py',
            'pattern': r'__version__ = "([0-9.]+)"',
        },
        {
            'name': '.bumpversion.cfg',
            'file': '.bumpversion.cfg',
            'pattern': r'current_version = ([0-9.]+)',
        },
        {
            'name': 'modmaker/pyproject.toml',
            'file': 'modmaker/pyproject.toml',
            'pattern': r'version = "([0-9.]+)"',
        }
    ]
    
    # Extract versions
    versions = {}
    for file_info in files_to_check:
        version = get_version_from_file(file_info['file'], file_info['pattern'])
        versions[file_info['name']] = version
    
    # Get PyPI version
    pypi_version = get_pypi_version()
    versions['PyPI'] = pypi_version
    
    # Display versions
    print(Fore.CYAN + "Version Information:" + Style.RESET_ALL)
    for name, version in versions.items():
        if version is None:
            print(f"{name}: {Fore.YELLOW}Not found{Style.RESET_ALL}")
        else:
            print(f"{name}: {Fore.GREEN}{version}{Style.RESET_ALL}")
    
    # Check if all versions match
    primary_version = versions['pyproject.toml']
    mismatches = []
    for name, version in versions.items():
        if version is not None and version != primary_version:
            mismatches.append((name, version, primary_version))
    
    if mismatches:
        print(Fore.RED + "\nVersion Mismatches Detected:" + Style.RESET_ALL)
        for name, version, expected in mismatches:
            print(f"{name}: {Fore.RED}{version}{Style.RESET_ALL} (expected: {Fore.GREEN}{expected}{Style.RESET_ALL})")
        
        print(Fore.YELLOW + "\nRun 'python scripts/sync_versions.py' to synchronize all versions." + Style.RESET_ALL)
        return 1
    else:
        print(Fore.GREEN + "\nAll version files are consistent." + Style.RESET_ALL)
        return 0

if __name__ == "__main__":
    sys.exit(main())