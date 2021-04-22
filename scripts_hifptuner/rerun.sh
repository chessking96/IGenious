if [ "$1" = "" ] ; then
  echo "Argument missing."
  exit
fi
./scripts_hifptuner/restore.sh $1
./scripts_hifptuner/setup.sh $1 $1
./scripts_hifptuner/run.sh $1
