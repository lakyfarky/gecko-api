#!/bin/bash

# First argument: Pause duration in seconds
PAUSE_DURATION=$1

# Check if the pause duration argument is provided
if [ -z "$PAUSE_DURATION" ]
then
      echo "Please provide a pause duration in seconds as an argument."
      exit 1
fi

# Run the first script
echo "Running idena.py script..."
python3 idena.py

# Wait for the specified pause duration
echo "Pausing for $PAUSE_DURATION seconds..."
sleep $PAUSE_DURATION

# Run the second script (replace second_script.py with your actual script name)
echo "Running second script..."
python3 analyze.py

echo "Scripts execution completed."

# ./run.sh 60
# chmod +x run_scripts.sh