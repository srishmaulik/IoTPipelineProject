#!/bin/bash

# Stop all instances of simulator.py
pkill -f "python3 simulator.py"
pkill -f "python3 bias_simulator.py"
pkill -f "python3 constant_simulator.py"
pkill -f "python3 drift_simulator.py"
pkill -f "python3 outliers_simulator.py"

echo "All simulator instances stopped."
