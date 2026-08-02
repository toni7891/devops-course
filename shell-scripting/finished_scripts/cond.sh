# !/bin/bash

# read -p "Enter your name: " NAME
# echo "Hello $NAME!"
# read -p "Enter city: " CITY
# read -p "Enter country: " COUNTRY
# echo "You are from $CITY, $COUNTRY."


# read -p "Enter a note: " NOTE
# echo "[$(date)] $NOTE" >> notes.txt
# echo "Note saved to notes.txt"

# read -p "Enter a password: " -s PASSWORD
# echo -e "\nPassword saved. Length: ${#PASSWORD}"


# read -p "Path to file to check: " PATHFILE

# if [ -f "$PATHFILE" ]; then
#     echo "File exists: $PATHFILE"
# else
#     echo "File does not exist in $PATHFILE"
# fi

# read -p "Check if directory exists. Enter path: " DIRPATH

# if [ -d "$DIRPATH" ]; then
#     echo "Directory exists: $DIRPATH"
# else
#     echo "Directory does not exist: $DIRPATH"
#     echo "Creating directory: $DIRPATH"
#     mkdir -p "$DIRPATH"
#     echo "Directory created: $DIRPATH"
# fi

# A=15
# B=8

# if [ $A -gt $B ]; then
#     echo "A = $A, B = $B"
#     echo "A is greater than B"
# else
#     echo "A = $A, B = $B"
#     echo "B is greater than A"
# fi


# read -p "variable value or not: " VAR

# if [ -z "$VAR" ]; then
#     echo "Variable is empty"
# elif [ -n "$VAR" ]; then
#     echo "Variable has value: $VAR"
# fi

# USR=$(whoami)
# if [ "$USR" == "root" ]; then
#     echo "You are logged in as root."
# else 
#     echo "You are logged in as $USR."
# fi


# TIME=$(date +%H)

# read -p "Enter your name: " NAME
# if [ $TIME -ge 17 ] && [ $TIME -le 23 ]; then
#     echo "Good evening Mr. $NAME"

# elif [ $TIME -ge 12 ] && [ $TIME -lt 17 ]; then
#     echo "Good afternoon Mr. $NAME"

# elif [ $TIME -gt 0 ] && [ $TIME -lt 6 ]; then 
#     echo "Good night Mr. $NAME"

# else 
#     echo "Good morning Mr. $NAME"

# fi


# read -p "Your age: " AGE

# if [ $AGE -gt 0 ] && [ $AGE -lt 121 ]; then 
#     echo "valid age: $AGE"

# else 
#     echo "Age is not valid. Age must be between 1-120. "
# fi

# read -p "path to file: " PATH

# if [ -f $PATH ]; then
#     echo "File exist at: $PATH"
#     read -p "Do you want to overwrite the existing file? : [y/n] " PREM

#     if [ "$PREM" == "y" ]; then
#         echo "" > $PATH
    

#     else 
#         echo "File was not overwritten!"
#     fi

# else 
#     echo "File dose not exist creating now..."
#     echo "" > $PATH
#     echo "Done!"

# fi 

# DATE=$(date +%d/%m/%Y)

# echo "Choose an option:"
# echo "1) Show date"
# echo "2) show username"

# read -p "Your choice: " CHOICE

# if [ $CHOICE == 1 ]; then 
#     echo "Today is $DATE"

# elif [ $CHOICE == 2 ]; then 
#     echo "Username: $(whoami)"

# else 
#     echo "invalid choice!"

# fi


# CORRECT_USR="admin"
# CORRECT_PASS="admin123"

# read -p "Username: " USR
# read -p "Password: " -s PASS

# if [ $USR == $CORRECT_USR ] && [ $PASS == $CORRECT_PASS ]; then 
#     echo -e "\naccess granted! welcome admin"

# else 
#     echo "X Access denied! X"

# fi

# read -p "Enter Path to File to find: " FILENAME

# if [ -f $FILENAME ]; then 
#     echo "Found: $FILENAME"

# else 
#     echo -e "\nFile not found in specified path : FILENAME "
# fi


# read -p "Enter message: " MSG


# if echo $MSG | grep -qi "error" ; then 
#     echo "Error found in message: $MSG"
#     echo "[$(date)] $MSG" >> error.log
#     echo "Logged to error.log!"

# else 
#     echo "No error found in message: $MSG"
#     echo "[$(date)] $MSG" >> info.log
#     echo "Logged to info.log!"
# fi



# echo "=== File Manager ===" 
# echo "1) List files "
# echo "2) Create file "
# echo "3) Delete file "

# read -p "Choice: " CHOICE

# if [ $CHOICE == "1" ]; then
#     ls -la /tmp/my_lab/

# elif [ $CHOICE == "2" ]; then 
#     read -p "Name of file: " FILENAME
#     echo "" > /tmp/my_lab/$FILENAME
#     ls /tmp/my_lab/

# elif [ $CHOICE == "3" ]; then 
#     read -p "Name of file: " DELFILE
#     FILEPATH=/tmp/my_lab/$DELFILE
#         if [ -f $FILEPATH ]; then
#         echo "File exists in: $FILEPATH"
#         rm $FILEPATH
#         echo "File: $DELFILE Has been deleted! X"
#         fi

# else 
#     echo "Invalid choice! XXX"
# fi





