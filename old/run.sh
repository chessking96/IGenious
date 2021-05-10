if [ "$1" = "" ] ; then
  echo "Argument missing."
  exit
fi
cd $1
python2 -O ../../precimonious/scripts/dd2.py $1.bc search_$1.json config_$1.json
cd ..
