if [ "$1" = "" ]; then
  echo "Argument missing."
  exit
fi

rm -rf $1
mkdir $1
cp $1.c $1/
