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

# Instala as dependências
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
  echo "Error: Failed to install requirements."
  exit 1
fi
echo "Executing program with input file: $1"
python3 -m src.main "$1"

echo "Execution finished."

echo ""
echo "Choose an option:"
echo "1 - Execute generated file (examples/output_1.py)"
echo "2 - Exit"
read -p "Option: " user_choice

case "$user_choice" in
  1)
    echo "Running examples/output_1.py..."
    python3 examples/output_1.py
    ;;
  2)
    echo "Exiting."
    ;;
  *)
    echo "Invalid option. Exiting."
    ;;
esac