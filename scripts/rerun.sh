if [ "$1" = "" ] || [ "$2" = "" ] ; then
  echo "Argument missing."
  exit
fi
./scripts/restore.sh $1
./scripts/setup.sh $1 $2
./scripts/run.sh $1
