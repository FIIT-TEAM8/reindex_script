#!/bin/bash

# Start the Python program
python main.py

# Wait for the Python program to finish
wait

# Alter values in .env
current_value=$(awk -F "=" '/START_DOCUMENT/ {print $2}' .env)

increase_value=$(awk -F "=" '/UPDATE_DOCUMENTS/ {print $2}' .env)

new_value=$((current_value + increase_value))

echo $new_value

sed -i "s/START_DOCUMENT=$current_value/START_DOCUMENT=$new_value/g" .env

# Start the Python program again, until some condition is met
while [ $new_value -lt 4800000 ]; do
    python main.py
    wait
	current_value=$new_value
    new_value=$((current_value + increase_value))
    echo $new_value
    sed -i "s/START_DOCUMENT=$current_value/START_DOCUMENT=$new_value/g" .env
done
