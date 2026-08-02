NAME=$(whoami)
HOST=$(hostname)
TIME= $(date +"%y-%m-%d")
FILESOFTMP=$(ls -l /tmp | wc -l)
FREEDSKSPC=$(df -h /| cut -d' ' -f4 | tail -n 1)

echo "===== System Summary ====="
echo "User: $NAME"
echo "Hostname: $HOST"
echo "Date: $TIME"
echo "Files in /tmp: $FILESOFTMP"
echo "Free Disk Space: $FREEDSKSPC"