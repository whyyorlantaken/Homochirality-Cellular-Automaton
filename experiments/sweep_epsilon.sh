#!/bin/bash

# Usage: ./experiments/sweep_epsilon.sh base_config.yaml start_eps end_eps num_steps
# Example: ./experiments/sweep_epsilon.sh config.yaml 0.0 1.0 2

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <base_config.yaml> <start_n> <end_m> <steps_p>"
    exit 1
fi

BASE_CONFIG=$1
START=$2
END=$3
STEPS=$4
IC="achiral_majority_128"

SWEEP_DIR="experiments/sweep_${IC}_eps_${START}_to_${END}"

mkdir -p "$SWEEP_DIR"

# Calculate the increment
if [ "$STEPS" -le 1 ]; then
    STEP_SIZE=0
else
    STEP_SIZE=$(python3 -c "print(($END - $START) / ($STEPS - 1))")
fi

echo "Starting epsilon sweep from $START to $END in $STEPS steps..."
echo "Results will be saved in $SWEEP_DIR"

for (( i=0; i<$STEPS; i++ ))
do
    # Calculate current epsilon
    CURRENT_EPS=$(python3 -c "print($START + $i * $STEP_SIZE)")
    
    echo "------------------------------------------"
    echo "Step $i: Running with epsilon = $CURRENT_EPS"
    
    # Create a temporary config for this run inside the sweep directory
    TEMP_CONFIG="${SWEEP_DIR}/config_step_${i}.yaml"
    
    # Use python to update the epsilon value safely and ensure mode is 'constant'
    python3 -c "
import yaml
import sys

try:
    with open('$BASE_CONFIG', 'r') as f:
        data = yaml.safe_load(f)
    
    # Update values
    if 'chaos' not in data: data['chaos'] = {}
    data['chaos']['mode'] = 'constant'
    if 'constant' not in data['chaos']: data['chaos']['constant'] = {}
    data['chaos']['constant']['epsilon'] = float('$CURRENT_EPS')
    
    with open('$TEMP_CONFIG', 'w') as f:
        yaml.dump(data, f, default_flow_style=False)
except Exception as e:
    print(f'Error updating yaml: {e}')
    sys.exit(1)
"
    
    if [ $? -ne 0 ]; then
        echo "Failed to create config for step $i"
        continue
    fi
    
    # Run the simulation
    # We assume main.py is in the root and we are running from the root
    python3 main.py "$TEMP_CONFIG" -ic "$IC"
    
    # The simulation saves to data/time-evolution/constant-<EPS>_dist-<dist_type>
    # Since we cannot easily predict the exact float string formatting of Python,
    # we identify the most recently created directory in data/time-evolution
    LATEST_DIR=$(ls -td data/time-evolution/*/ 2>/dev/null | head -1)
    
    if [ -n "$LATEST_DIR" ]; then
        DEST_DIR="${SWEEP_DIR}/eps_${CURRENT_EPS}"
        mv "$LATEST_DIR" "$DEST_DIR"
        # Also move the temp config into the result folder for reference
        mv "$TEMP_CONFIG" "$DEST_DIR/config.yaml"
        echo "Saved results to $DEST_DIR"
    else
        echo "Warning: Could not find output directory for step $i"
    fi
done

echo "------------------------------------------"
echo "Sweep complete. All results are in $SWEEP_DIR"
