#!/bin/bash
# Script to prepare testing environment for GitHub Actions

# Make sure the bin/modmaker script is executable
echo "Setting executable permissions on bin/modmaker"
chmod +x modmaker/bin/modmaker

# Verify the file exists and is executable
if [ -x modmaker/bin/modmaker ]; then
    echo "Verified: modmaker/bin/modmaker is executable"
else
    echo "ERROR: modmaker/bin/modmaker is not executable or does not exist"
    exit 1
fi

# Set up Python path for imports
export PYTHONPATH=$(pwd):$PYTHONPATH
echo "PYTHONPATH is now: $PYTHONPATH"

# Print structure to debug
echo "Project structure:"
find . -type f -name "*.py" | grep -v "__pycache__" | sort

# Run the help command to check if script works
echo "Testing bin/modmaker:"
python modmaker/bin/modmaker --help || echo "Warning: Direct execution failed"

echo "Test environment setup complete"