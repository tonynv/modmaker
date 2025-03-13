#!/usr/bin/env python3
"""
Script to synchronize version numbers across different files.
"""

import re
import os
import sys
import subprocess

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

def update_file(file_path, pattern, replacement):
    """Update a file with the new version."""
    if not os.path.exists(file_path):
        print(f"Warning: File {file_path} does not exist. Skipping.")
        return False
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    updated_content = re.sub(pattern, replacement, content)
    
    if content != updated_content:
        with open(file_path, 'w') as file:
            file.write(updated_content)
        print(f"Updated {file_path}")
        return True
    else:
        print(f"No changes needed for {file_path}")
        return False

def main():
    """Main function to synchronize versions."""
    # Get the target version
    if len(sys.argv) > 1:
        target_version = sys.argv[1]
        print(f"Using specified version: {target_version}")
    else:
        target_version = get_pypi_version()
        
        if not target_version:
            print("Error: Could not determine PyPI version.")
            sys.exit(1)
    
    print(f"Synchronizing all files to version {target_version}")
    
    # Define patterns and replacements for each file
    updates = [
        # pyproject.toml
        {
            'file': 'pyproject.toml',
            'pattern': r'version = "([0-9.]+)"',
            'replacement': f'version = "{target_version}"'
        },
        # setup.cfg
        {
            'file': 'setup.cfg',
            'pattern': r'version = ([0-9.]+)',
            'replacement': f'version = {target_version}'
        },
        # __init__.py
        {
            'file': '__init__.py',
            'pattern': r'__version__ = "([0-9.]+)"',
            'replacement': f'__version__ = "{target_version}"'
        },
        # modmaker/__init__.py
        {
            'file': 'modmaker/__init__.py',
            'pattern': r'__version__ = "([0-9.]+)"',
            'replacement': f'__version__ = "{target_version}"'
        },
        # .bumpversion.cfg
        {
            'file': '.bumpversion.cfg',
            'pattern': r'current_version = ([0-9.]+)',
            'replacement': f'current_version = {target_version}'
        },
        # Check for modmaker/pyproject.toml if it exists
        {
            'file': 'modmaker/pyproject.toml',
            'pattern': r'version = "([0-9.]+)"',
            'replacement': f'version = "{target_version}"'
        }
    ]
    
    updated = False
    for update in updates:
        file_updated = update_file(update['file'], update['pattern'], update['replacement'])
        updated = updated or file_updated
    
    if updated:
        print(f"Successfully synchronized all files to version {target_version}")
        
        # Create git commit if requested
        auto_commit = False
        for arg in sys.argv:
            if arg == "--commit":
                auto_commit = True
                
        if auto_commit:
            subprocess.run(['git', 'add', '.'], check=False)
            subprocess.run(['git', 'commit', '-m', f'Synchronize version to {target_version}'], check=False)
            print("Created git commit with version changes")
        elif sys.stdout.isatty():  # Only ask for input in interactive mode
            try:
                create_commit = input("Create git commit with these changes? (y/n): ")
                if create_commit.lower() == 'y':
                    subprocess.run(['git', 'add', '.'], check=False)
                    subprocess.run(['git', 'commit', '-m', f'Synchronize version to {target_version}'], check=False)
                    print("Created git commit with version changes")
            except (EOFError, KeyboardInterrupt):
                pass
    else:
        print("All files already at the correct version")

if __name__ == "__main__":
    main()