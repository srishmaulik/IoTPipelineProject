#!/bin/bash

# Stop all instances of simulator.py
pkill -f "python3 kafkaToCassandra.py"

echo "All consumer instances stopped."
