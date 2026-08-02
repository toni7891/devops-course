#!/bin/bash

IS_IT=2
YEAR=0

read -p "what year is it: " YEAR

check_leap(){
    TO_CHECK=$1
    if [ $(( $TO_CHECK % 400)) -eq 0 ]; then
        IS_IT=1
    elif [ $(( $TO_CHECK % 100 )) -eq 0 ]; then
        IS_IT=0
    elif [ $(( $TO_CHECK % 4 )) -eq 0 ]; then
        IS_IT=1
    else 
        IS_IT=0
    fi
}

check_leap $YEAR

if [ $IS_IT -eq 1 ]; then
    echo "$YEAR is a leap year!"

elif [ $IS_IT -eq 0 ]; then
    echo "$YEAR is NOT a leap year! XXX"

else 
    echo "XXX----ERROR has occured!----XXX"
fi


