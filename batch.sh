#!/bin/bash

timestamp=$(date +"%Y%m%d%H%M%S")
result_file="resultats_$timestamp.csv"

echo "Protocol,Message Length,Message Count,sleep,receivers,Total Time,Average" >> "$result_file"

echo "--------------------IVY------------------" >> "$result_file"
sleep=0
receivers=1

for length in 5 500 1000 2000 3000
do

	for ((message_count=5000; message_count<=30000; message_count+=5000)); do

		result=$(python3 main.py --protocol ivy --message_count $message_count --port 10.34.127.255:4912 --length $length --log_level FATAL | tail -n 2)
	    total_time=$(echo "$result" | awk '{print $9}')
	    average=$(echo "$result"| tail -n 1 | awk '{print $4}')
        echo "IVY,$length,$message_count,$sleep,$receivers,$total_time,$average" >> "$result_file"

	done
    message_count=75000
    result=$(python3 main.py --protocol ivy --message_count $message_count --port 10.34.127.255:4912 --length $length --log_level FATAL | tail -n 2)
    total_time=$(echo "$result" | awk '{print $9}')
    average=$(echo "$result"| tail -n 1 | awk '{print $4}')
    echo "IVY,$length,$message_count,$sleep,$receivers,$total_time,$average" >> "$result_file"

	for ((message_count=100000; message_count<=1000000; message_count+=100000)); do

		result=$(python3 main.py --protocol ivy --message_count $message_count --port 10.34.127.255:4912 --length $length --log_level FATAL | tail -n 2)
	    total_time=$(echo "$result" | awk '{print $9}')
	    average=$(echo "$result"| tail -n 1 | awk '{print $4}')
        echo "IVY,$length,$message_count,$sleep,$receivers,$total_time,$average" >> "$result_file"
	done
done

echo "--------------------ZeroMQ------------------" >> "$result_file"


for length in 5 500 1000 2000 3000
do
	echo "Envoi de batchs de messages sans sleep de $length caractères avec zeromq" >> "$result_file"
	for ((message_count=5000; message_count<=30000; message_count+=5000)); do

		result=$(python3 main.py --protocol zeromq --message_count $message_count --port 10.34.127.255:4912 --length $length --log_level FATAL | tail -n 2)
	    total_time=$(echo "$result" | awk '{print $9}')
	    average=$(echo "$result"| tail -n 1 | awk '{print $4}')
        echo "ZeroMQ,$length,$message_count,$sleep,$receivers,$total_time,$average" >> "$result_file"
	done

    message_count=75000
		result=$(python3 main.py --protocol zeromq --message_count $message_count --port 10.34.127.255:4912 --length $length --log_level FATAL | tail -n 2)
	    total_time=$(echo "$result" | awk '{print $9}')
	    average=$(echo "$result"| tail -n 1 | awk '{print $4}')
        echo "ZeroMQ,$length,$message_count,$sleep,$receivers,$total_time,$average" >> "$result_file"

	for ((message_count=100000; message_count<=1000000; message_count+=100000)); do

		result=$(python3 main.py --protocol zeromq --message_count $message_count --port 10.34.127.255:4912 --length $length --log_level FATAL | tail -n 2)
	    total_time=$(echo "$result" | awk '{print $9}')
	    average=$(echo "$result"| tail -n 1 | awk '{print $4}')
        echo "ZeroMQ,$length,$message_count,$sleep,$receivers,$total_time,$average" >> "$result_file"
	done
done

message_count=100000
length=3000
for ((receivers=1; receivers<=20; receivers+=1)); do

    result=$(python3 main.py --protocol ivy --message_count $message_count --nbr_processes $receivers --port 10.34.127.255:4912 --length $length --log_level FATAL | tail -n 2)
    total_time=$(echo "$result" | awk '{print $9}')
    average=$(echo "$result"| tail -n 1 | awk '{print $4}')
    echo "ivy,$length,$message_count,$total_time,$average" >> "$result_file"
done

for ((receivers=1; receivers<=20; receivers+=1)); do

    result=$(python3 main.py --protocol zeromq --message_count $message_count --nbr_processes $receivers --port 10.34.127.255:4912 --length $length --log_level FATAL | tail -n 2)
    total_time=$(echo "$result" | awk '{print $9}')
    average=$(echo "$result"| tail -n 1 | awk '{print $4}')
    echo "ZeroMQ,$length,$message_count,$total_time,$average" >> "$result_file"
done

for length in 5 500 1000 2000 3000
do
	for ((message_count=1000; message_count<=10000; message_count+=1000)); do

		result=$(python3 main.py --protocol ivy --message_count $message_count --port 10.34.127.255:4912 --length $length --direct_msg --log_level FATAL | tail -n 2)
	    total_time=$(echo "$result" | awk '{print $9}')
	    average=$(echo "$result"| tail -n 1 | awk '{print $4}')
        echo "IVY,$length,$message_count,$sleep,$receivers,$total_time,$average" >> "$result_file"
