#/bin/sh

ps aux | grep -q '[s]ocat TCP-LISTEN:6000'
if [ $? -ne 0 ]; then
    echo "Starting socat"
    socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\" &
fi
ps aux | grep -q '[X]Quartz'
if [ $? -ne 0 ]; then
    echo "Starting XQuartz"
    open -a XQuartz
fi
echo "IP=`ipconfig getifaddr en0`" > .env
docker-compose up -d
docker exec -it python-tk python 1-trees/binary_tree.py
