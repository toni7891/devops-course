#!/bin/bash

for user in $(grep -v '^#' /etc/passwd | cut -d: -f1); do
    echo "$user"
done


