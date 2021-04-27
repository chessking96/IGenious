if [ "$1" = "" ]; then
  echo "Argument missing."
  exit
fi


docker start hi
docker exec hi rm -rf /root/$1
docker exec hi mkdir /root/$1
docker cp scripts_hifptuner/to30.sh hi:/root
docker cp scripts_hifptuner/to38.sh hi:/root
docker cp $1/$1.c hi:/root/$1/$1.c
