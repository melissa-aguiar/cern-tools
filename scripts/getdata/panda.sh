#!/bin/sh

inds=${1:-""}
suff=${2:-"h2000.v1"}
jo=${3:-"h2000.py"}
op=${4:-""}
nick="user.$USER"

if [ -z "$inds" ]
then echo Input dataset is not set
     exit 1
fi

if [ -r $inds ]
then inds=`cat $inds`
fi

touch job.log
echo >> job.log
echo >> job.log
echo `date` >> job.log
touch tocheck

echo $inds
echo $nick

for inDS in `echo $inds`
do  
  if [ -z "$op" ]
  then opt=""
  else opt="-c '$op'"
  fi
  out=`echo ${inDS} | cut -d\/ -f1 | sed "s|$nick\.||g" `.${suff}
  pathena \
    --excludeFile=log\*,test\*,dataset\*,user.\*,\*.log,\*.tmp,\*.dat,\*.txt,\*.root,\*.sh,\*RAW\*,panda.\* \
    --inDS=${inDS} \
    --outDS=${nick}.${out} \
    --nFiles=2000\
    --nGBPerJob=14 \
	$opt $jo \
      > job.tmp 2>&1
  echo >> job.log
  cat job.tmp >> job.log
  grep jediTaskID job.tmp | cut -d\= -f2 >> tocheck
done

