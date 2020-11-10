cd /unix/atlas3/avalee/2DMVA/run

for file in `grep -l "Killed" *.o*`
do
  jobName="$(echo $file | cut -d'_' -f-3)"
  filename=`echo "Eval_${jobName}.sh"`
  echo $filename
  cd /unix/atlas3/avalee/2DMVA/
  qsub -N ${jobName}_Eval -q medium -l mem=24gb -j oe batch_submit/$filename
done
