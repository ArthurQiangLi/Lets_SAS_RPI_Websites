#!/bin/bash
#How to use it?
#1. chmod +x stressng_ramp_up.sh  -----> to make this script executable
#2. ./ramp_up_stress.sh   -----> to execute it


# Total duration of stress in seconds
TOTAL_DURATION=600

# Ramp-up duration in seconds
RAMP_UP_DURATION=180

# Target CPU load percentage
CPU_TARGET_LOAD=70

# Target memory usage in MB (adjust based on your calculation)
MEMORY_TARGET_MB=270

# Number of CPU cores
CPU_CORES=4

# Step interval for increasing load (in seconds)
STEP_INTERVAL=10

# Calculate the load increment per step
LOAD_INCREMENT=$((CPU_TARGET_LOAD / (RAMP_UP_DURATION / STEP_INTERVAL)))

# Initialize current load
CURRENT_LOAD=0

# Gradually increase the load
while [ "$CURRENT_LOAD" -lt "$CPU_TARGET_LOAD" ]; do
    echo "Ramping up to ${CURRENT_LOAD}% CPU load..."
    stress-ng --cpu $CPU_CORES --cpu-load $CURRENT_LOAD --vm 1 --vm-bytes "${MEMORY_TARGET_MB}M" --timeout "$STEP_INTERVAL"s &
    sleep $STEP_INTERVAL
    CURRENT_LOAD=$((CURRENT_LOAD + LOAD_INCREMENT))
done

# Maintain the target load for the remaining time
REMAINING_TIME=$((TOTAL_DURATION - RAMP_UP_DURATION))
echo "Maintaining ${CPU_TARGET_LOAD}% CPU load for ${REMAINING_TIME} seconds..."
stress-ng --cpu $CPU_CORES --cpu-load $CPU_TARGET_LOAD --vm 1 --vm-bytes "${MEMORY_TARGET_MB}M" --timeout "${REMAINING_TIME}s"

echo "Stress test completed."
