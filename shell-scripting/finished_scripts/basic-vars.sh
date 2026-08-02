#!/bin/bash

OSNAME=$(sw_vers | head -n 1 | cut -d: -f2)
OSVERSION=$(sw_vers | sed -n '2p' | cut -d: -f2)
UPTIME=$(uptime | cut -dl -f1)
BIGFILE=$(du -sh /Users/tonyverin/Desktop/* | sort -rh | head -n 1)
PATHOFUSR=/Users/tonyverin/Desktop/
NOTE=/tmp/notes.txt
USRLO=$(whoami | tr '[:upper:]' '[:lower:]') 
USRUP=$(whoami | tr '[:lower:]' '[:upper:]')
IPADDR=$(ipconfig getifaddr en0)
HEADER="System Report"
LENHEAD=${#HEADER}


echo "I am: $0"
echo "Total users on system: $(cat /etc/passwd | wc -l)"
echo "OS: $OSNAME $OSVERSION"
echo "System has been running for: $UPTIME"
echo "Biggest file in /Desktop: $BIGFILE"
echo $PATHOFUSR | cut -d/ -f3
echo "File: $NOTE"
echo "Size: $(du -sh $NOTE | cut -f -1)"
echo "Lines: $(wc -l $NOTE | awk '{ print $1 }')"
echo "Words: $(wc -w $NOTE | awk '{ print $1 }')"
echo "Modified: $(date -r $NOTE)"
echo "lower usr: $USRLO"
echo "UPPER usr: $USRUP"
echo "IP address: $IPADDR"
printf '=%.0s' $(seq 1 $LENHEAD)
echo -e "\n$HEADER"
printf '=%.0s' $(seq 1 $LENHEAD)
echo