#!/bin/bash

timestamp=$(date +"%Y%m%d%H%M%S")
result_file="resultats_$timestamp.csv"

echo "Protocol,Message Length,Message Count,Total Time,Average" >> "$result_file"

echo "--------------------IVY------------------"

for length in 5 
do
    echo
    echo "Envoi de batchs de messages sans sleep de $length caractères avec IVY"
    echo

    for message_count in 5000 
    do
        echo "avec $message_count messages:"
        result=$(python3 main.py --protocol ivy --message_count $message_count --port 10.34.127.255:1764 --length $length --log_level FATAL | tail -n 2)
	    total_time=$(echo "$result" | awk '{print $9}')
	    average=$(echo "$result"| tail -n 1 | awk '{print $4}')
	
        echo "IVY,$length,$message_count,$total_time,$average" >> "$result_file"
        echo
    done

    

   
done

