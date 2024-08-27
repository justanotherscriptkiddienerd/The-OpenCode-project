#!/bin/bash

# Ask the user for the directory path
read -p "Please enter the directory path of the project's directory (i.e. /root/opencode): " program_dir

# Check if the directory exists
if [ -d "$program_dir" ]; then
    # Navigate to the directory
    cd "$program_dir" || { echo "Failed to navigate to the directory."; exit 1; }
    echo "Successfully navigated to $program_dir"
    echo Starting download...
    git clone https://github.com/justanotherscriptkiddienerd/The-OpenCode-project.git
    echo Download complete
    echo Starting cleanup
    rm -r "$program_dir"
    echo Old dir removed
    echo Done. The Directory is now /root/The-Opencode-Project Or your custom path.
else
    # Print an error if the directory does not exist
    echo "The directory '$program_dir' does not exist."
    exit 1
fi
