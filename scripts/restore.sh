
# argumetns: path, filename
if [ "$2" = "" ]; then
  echo "Argument missing."
  exit
fi

rm -rf $1/analysis
mkdir $1/analysis
cp $1/$2 $1/analysis/$2

echo $2 restored.
