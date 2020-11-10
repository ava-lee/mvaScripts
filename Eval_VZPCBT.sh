#usage: source ....sh [number of jets]
#e.g. source ....sh 3
mkdir batch_submit

for i in $(seq 1 1 4)
do

echo "Depth = $i"

filename=$(echo "Eval_PCBTVZ_Depth${i}.sh")

echo "Create "$filename

rm -rf batch_submit/$filename
touch batch_submit/$filename

echo "export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
. ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh  --quiet
cd /unix/atlas3/avalee/thesisMVA/
setupATLAS
cd build/
asetup --restore
source */setup.sh
cd ../run" >> batch_submit/$filename

echo "EvaluateMVA -w '/unix/atlas3/avalee/MVA/run/dataloader_BDT_1L_2J_150ptv_1of2_PCBT200_2J_Depth_${i}/weights/TMVAClassification_BDT_1L_2J_150ptv_1of2.weights.xml:/unix/atlas3/avalee/MVA/run/dataloader_BDT_1L_3J_150ptv_1of2_PCBT200_3J_Depth_${i}/weights/TMVAClassification_BDT_1L_3J_150ptv_1of2.weights.xml' -s Diboson -a 1 -k 2 -l 2jet:3jet -r '(nJ>1.5&&nJ<2.5):(nJ>2.5&&nJ<3.5)'  -v 'pTV:MET:dPhiVBB:pTB1:pTB2:mBB:dRBB:dPhiLBmin:mTW:Mtop:dYWH:bin_MV2c10B1:bin_MV2c10B2;pTV:MET:dPhiVBB:pTB1:pTB2:mBB:dRBB:dPhiLBmin:mTW:Mtop:dYWH:bin_MV2c10B1:bin_MV2c10B2:mBBJ:pTJ3' -d /unix/atlas3/avalee/MVA/LPNHE_1lep_hybridtruthtag_32-07_PCB/ -c 'VZPCBT_Depth${i}'" >> batch_submit/$filename

chmod a+xwr batch_submit/$filename

qsub -V -N "Eval_PCBTVZ_Depth${i}" -q medium -l mem=24gb -j oe batch_submit/$filename

done