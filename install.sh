#!/bin/bash

# Create scripts directory if it doesn't exist
mkdir -p scripts

# Clone AutomateSQLC into scripts folder
git clone https://github.com/yourusername/AutomateSQLC.git scripts/AutomateSQLC

# Navigate to AutomateSQLC directory
cd scripts/AutomateSQLC

# Install Python dependencies
pip install -r requirements.txt

echo "AutomateSQLC has been installed successfully!"