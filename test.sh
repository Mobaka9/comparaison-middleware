#!/bin/bash

timestamp=$(date +"%Y_%m_%d %H:%M:%S")
result_file="resultatsp2vsp7_$timestamp.csv"

echo "Protocol,Message Length,Message Count,sleep,receivers,Total Time,Average" >> "$result_file"

echo "--------------------IVY------------------" >> "$result_file"
sleep=0
message_count=100000
length=3000

for ((receivers=1; receivers<=20; receivers+=1)); do

    result=$(python3 main.py --protocol ivy --nbr_processes $receivers --message_count $message_count --port 10.34.127.255:4912 --length $length --log_level FATAL | tail -n 1)
    total_time=$(echo "$result" | awk '{print $13}')
    #average=$(echo "$result"| tail -n 1 | awk '{print $4}')
    echo "ivy,$length,$message_count,$total_time,$average" >> "$result_file"
done