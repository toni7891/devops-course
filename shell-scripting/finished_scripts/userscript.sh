#!/bin/bash

USERNAME=$(whoami)
DATE=$(date)
SYSINFO=$(hostname)
DSKSPC=$(df -h /)
YMD=$(date +%Y-%m-%d)
TEXT="devops"

echo -e "Hello, $USERNAME! Welcome to the world of shell scripting.\n"
echo -e "\n$DATE - This script is running successfully!\n"
echo -e "Your system information: $SYSINFO"
#mkdir -p /tmp/my_lab && echo -e "\nDirectory /tmp/my_lab created successfully!\n" || echo -e "\nFailed to create directory /tmp/my_lab\n"
#touch /tmp/my_lab/notes.txt 
echo -e "\nFile created. contents:\nthis is my first file\n" > /tmp/my_lab/notes.txt && cat /tmp/my_lab/notes.txt
echo -e "Files in /tmp:\n$(ls -lh /tmp)\n"
echo -e "\nDisk usage:\n$DSKSPC\n"
echo -e "\nNumber of files in /tmp: $(ls -lh /tmp | wc -l)\n"
echo -e "Size of vars.sh: $(du -sh vars.sh)\n"
#echo -e "Second line added by script" >> script.sh && cat script.sh
echo -e "Found matching line:\n$(grep -i Second script.sh)\n"
echo -e "Today's date: $YMD\n"
#mv script.sh script_$YMD.sh && echo -e "Script renamed to script_$YMD.sh\n"
echo -e "\nThis script is called: $0\n"
echo -e "The text variable: $TEXT\n"
echo -e "The text variable reversed: $(echo $TEXT | rev)\n"
sed 's/two/original/' forreplace.txt > forreplace.txt && cat forreplace.txt





