# run in folder with txt files
# source ...sh [algorithm]

for file in *.o*; do
  mv $file ${file::(-8)}txt
done

for file in `grep -l "<BookMVA> fatal error" *.txt`; do mv $file incomplete/$file; done

rm /unix/atlas3/avalee/2DMVA/MVAScripts/sigs_${1}_medPTV.txt
touch /unix/atlas3/avalee/2DMVA/MVAScripts/sigs_${1}_medPTV.txt
for file in `find . -maxdepth 1 -type f -name "${1}*_medPTV_*.txt" | sort -n`
do
  echo "${file}" >> /unix/atlas3/avalee/2DMVA/MVAScripts/sigs_${1}_medPTV.txt
  python /unix/atlas3/avalee/2DMVA/MVAScripts/calculateSig_medpTV.py $file >> /unix/atlas3/avalee/2DMVA/MVAScripts/sigs_${1}_medPTV.txt
done
