#!/bin/bash

read -p "Choice: " ORDER

case $ORDER in
    'Vanilla')
        echo "Order is Vanilla" 
        ;;
    'Chocolate')
        echo "Order is Chocolate" 
        ;;
    'Burger')
        echo "Order is Burger" 
        ;;
esac