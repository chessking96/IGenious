if [ "$1" = "" ] ; then
  echo "Argument missing."
  exit
fi
./scripts/restore.sh $1
./scripts/setup.sh $1 $1
./scripts/run.sh $1
