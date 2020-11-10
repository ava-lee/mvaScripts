cd /unix/atlas3/avalee/2DMVA/

for file in `grep -l "Killed" *.o*`
do
  jobName="$(echo $file | cut -d'_' -f-3)" #-3 for high pTV, -5 for medium pTV
  filename=`echo "${jobName}.sh"`
  echo $filename
  cd /unix/atlas3/avalee/2DMVA/
  #qsub -N ${jobName} -q medium -l mem=24gb -j oe batch_submit/$filename
done

for file in `grep -L "Finalise MVA Training" *.o*`
do
  #for file in *.o*; do mv $file ${file//medpTV/medPTV}; done
  jobName="${file%.*}"
  filename=`echo "${jobName}.sh"`
  echo $filename
  cd /unix/atlas3/avalee/2DMVA/
  qsub -N ${jobName} -q medium -l mem=24gb -j oe batch_submit/$filename
done