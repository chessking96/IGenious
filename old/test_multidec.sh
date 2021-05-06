if [ "$1" = "" ] ; then
  echo "Argument missing."
  exit
fi
cd $1
python3 ../multideclaration.py DFT16
cd ..