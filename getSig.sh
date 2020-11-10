# run in folder with txt files
# source ...sh [algorithm]

for file in *.o*; do
  mv $file ${file::(-8)}txt
done

for file in `grep -l "<BookMVA> fatal error" *.txt`; do mv $file incomplete/$file; done

rm /unix/atlas3/avalee/2DMVA/MVAScripts/sigs_${1}.txt
touch /unix/atlas3/avalee/2DMVA/MVAScripts/sigs_${1}.txt
for file in `find . -maxdepth 1 -type f -name "${1}*.txt" | sort -n`
do
  echo "${file}" >> /unix/atlas3/avalee/2DMVA/MVAScripts/sigs_${1}.txt
  python /unix/atlas3/avalee/2DMVA/MVAScripts/calculateSig.py $file >> /unix/atlas3/avalee/2DMVA/MVAScripts/sigs_${1}.txt
done
