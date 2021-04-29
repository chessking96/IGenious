
# arguments: path, filename, functionname, filename (only for now, without extension)
if [ "$4" = "" ] ; then
  echo "Argument missing."
  exit
fi
./scripts/restore.sh $1 $2


# Prepare Setup
if python3 $SOURCE_PATH/scripts/setup.py $1 $2 $3; then
  echo 'Setup succeeded'
else
  echo 'Setup failed'
  exit
fi

# Run
cd $1/analysis
if python2 -O $CORVETTE_PATH/scripts/dd2.py $4.bc search_$4.json config_$4.json $1 $4; then
  echo 'Run succeeded'
else
  echo 'Run failed'
  exit
fi
