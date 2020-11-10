#usage: source ....sh [number of jets]
#e.g. source ....sh 3
cd /unix/atlas3/avalee/2DMVA/
mkdir batch_submit

for i in $(seq 1 1 4)
do

echo "Depth = $i"

for j in $(seq 200 200 1000)
do

echo "Trees = $j"

filename=$(echo "Eval_Grad0.5_Depth${i}_${j}_medPTV.sh")

echo "Create "$filename

rm -rf batch_submit/$filename
touch batch_submit/$filename

echo "export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
. ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh  --quiet
cd /unix/atlas3/avalee/2DMVA/
setupATLAS
cd build/
asetup --restore
source */setup.sh
cd ../run" >> batch_submit/$filename

echo "EvaluateMVA -w './dataloader_BDT_1L_2J_75ptv_150ptv_1of2_Grad0.5_Depth${i}_${j}/weights/TMVAClassification_BDT_1L_2J_75ptv_150ptv_1of2.weights.xml:./dataloader_BDT_1L_3J_75ptv_150ptv_1of2_Grad0.5_Depth${i}_${j}/weights/TMVAClassification_BDT_1L_3J_75ptv_150ptv_1of2.weights.xml' -a 1 -k 2 -l "2jet:3jet" -r '(nJ>1.5&&nJ<2.5):(nJ>2.5&&nJ<3.5)' -d /unix/atlas3/avalee/MVA/LPNHE_1lep_hybridtruthtag_32-07/ -c 'Grad0.5_Depth${i}_${j}_medPTV'" >> batch_submit/$filename

chmod a+xwr batch_submit/$filename

qsub -N "Grad0.5_Depth${i}_${j}_medPTV_Eval" -q medium -l mem=24gb -j oe batch_submit/$filename

done
done