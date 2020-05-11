#!/bin/bash

if [ -f $1 ]
then
    touch info
    num_lines=$(wc $1 | awk '{print $1}')
    echo "Number of lines in a file: " $num_lines
    echo $num_lines > info

    echo "------------------------------------"
    echo "------------------------------------" >> info

    for item in $(cat $1 | awk '{print $6}' | sort -u | cut -c 2-)
    do
        num_items=$(grep $item $1 | wc -l)
        echo "Number of lines with " $item ": " $num_items
        echo $item $num_items >> info
    done

    echo "------------------------------------"
    echo "------------------------------------" >> info

    echo "Top 10 biggest requests:"
    echo "$(cat $1 | awk '{print substr($6,2), $7, $1, substr($4,2) , $10}' | sort -nrk5  | head -n 10)"
    echo "$(cat $1 | awk '{print substr($6,2), $7, $1, substr($4,2) , $10}' | sort -nrk5  | head -n 10)" >> info


    echo "------------------------------------"
    echo "------------------------------------" >> info

    echo "Top 10 mas counter requests with client error:"
    echo "$(cat $1 | awk '{if (($9>=400) && ($9<500)) print substr($6,2), $7, $9, $1}' | sort -rnk4 | uniq -d -c | sort -rnk1 | head -n 10 | awk '{ print ($2), $3, $4, $5}')"
    echo "$(cat $1 | awk '{if (($9>=400) && ($9<500)) print substr($6,2), $7, $9, $1}' | sort -rnk4 | uniq -d -c | sort -rnk1 | head -n 10 | awk '{ print ($2), $3, $4, $5}')" >> info

    echo "------------------------------------"
    echo "------------------------------------" >> info

    echo "Top 10 biggest requests with client error:"
    echo "$(cat $1 | awk '{if (($9>=400) && ($9<500)) print substr($6,2), $7, $9, $1, $10}' | sort -nrk5 -k4  | awk '{print $1, $2, $3, $4}' | head -n 10)"
    echo "$(cat $1 | awk '{if (($9>=400) && ($9<500)) print substr($6,2), $7, $9, $1, $10}' | sort -nrk5 -k4  | awk '{print $1, $2, $3, $4}' | head -n 10)" >> info

    exit 0

else
    echo "log file not found"
    exit 1
fi
