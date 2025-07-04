#!/bin/bash

if [ -z "$1" ]; then
  echo "Error: You must provide the path to the input file."
  echo "Usage: ./run_program.sh <path/to/input_file.txt>"
  exit 1
fi

source .venv/bin/activate
if [ $? -ne 0 ]; then
 echo "Error: Could not activate the virtual environment. Check the path or permissions."
 exit 1
fi

echo "Executing program with input file: $1"
python3 -m src.main "$1"

echo "Execution finished."