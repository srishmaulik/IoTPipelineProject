#!/bin/bash

# Check if a configuration file is provided

# Read the configuration file
config_file="simulators.conf"

# Check if the configuration file exists
if [ ! -f "$config_file" ]; then
    echo "Error: Configuration file not found."
    exit 1
fi

shared_count=0

# Loop through each line in the configuration file
while IFS=, read -r program count; do
    # Skip comments and empty lines
    if [[ "$program" == \#* || -z "$program" ]]; then
        continue
    fi

    # Validate that count is a positive integer
    if ! [[ "$count" =~ ^[0-9]*$ ]]; then
        echo "Error: Invalid count for $program. Count must be a positive integer."
        continue
    fi

    # Launch instances of the program based on the count
    for ((i = 1; i <= count; i++)); do
        ((shared_count++))
        python3 "$program" "$shared_count" &  # Replace with the actual command to launch the program
   	sleep 0.06	
    done

done < "$config_file"

echo "Program instances launched based on the configuration file."
