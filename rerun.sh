if [ "$1" = "" ] ; then
  echo "Argument missing."
  exit
fi
./restore.sh $1
./setup.sh $1 $1
./run.sh $1
