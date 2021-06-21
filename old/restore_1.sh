if [ "$1" = "" ]; then
  echo "Argument missing."
  exit
fi


docker start hi
docker exec hi rm -rf /root/$1
docker exec hi mkdir /root/$1
docker cp $1.c hi:/root/$1/$1.c

# move this later into Dockerfile
docker exec hi sed -i 's/$auto_tuning/\/root\/HiFPTuner/g' /root/HiFPTuner/scripts/compile.sh
docker exec hi sed -i 's/$auto_tuning/\/root\/HiFPTuner/g' /root/HiFPTuner/scripts/analyze.sh
docker exec hi sed -i 's/-llog//g' /root/HiFPTuner/scripts/analyze.sh
