#!/bin/bash

BOT_ADDR=pi@192.168.43.229

for file in $*
do
    scp $file $BOT_ADDR:~/firstbot/$file
done

    
