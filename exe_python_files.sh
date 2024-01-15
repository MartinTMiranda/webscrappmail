#!/bin/bash

# Define an array of file names
files=("./wong2.py" "./tailoy.py" "./hiraoka.py" "./tottus.py" "./saga.py" "./send_email_2.py")

# Iterate over the array and execute each file
for file in "${files[@]}"
do
    sudo python3.8 "$file"
done
