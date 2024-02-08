#!/bin/bash

# Check for correct number of arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <IP_address> <number_of_instances>"
    exit 1
fi

IP_ADDRESS=$1
NUM_INSTANCES=$2

# Loop to execute kafkaToCassandra.py script
for ((i=1; i<=$NUM_INSTANCES; i++)); do
    echo "Running instance $i"
    python3 kafkaToCassandra.py "$IP_ADDRESS" &
done

echo "Started $NUM_INSTANCES instances of kafkaToCassandra.py"
