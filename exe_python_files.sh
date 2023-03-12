#!/bin/bash

# Define an array of file names
files=("/home/userland/wong2.py" "/home/userland/tailoy.py" "/home/userland/hiraoka.py" "/home/userland/tottus.py" "/home/userland/saga.py" "/home/userland/send_email_2.py")

# Iterate over the array and execute each file
for file in "${files[@]}"
do
    sudo python3.8 "$file"
done
