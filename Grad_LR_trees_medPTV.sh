#usage: source ....sh [number of jets]
#e.g. source ....sh 3
cd /unix/atlas3/avalee/2DMVA/
mkdir batch_submit

for i in $(seq 0.1 0.05 0.7)
do

echo "Learning rate = $i"

for j in $(seq 200 100 800)
do

echo "Trees = $j"

filename=$(echo "Grad_${i}_${j}_${1}_medPTV.sh")

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

echo "RunMVATraining -d /unix/atlas3/avalee/MVA/SMU_1lep_truthtag_32-07/ -a 1 -s VH -m $1 -x $1 -l 75 -u 150 -H '!H:!V:NTrees=$j:MaxDepth=4:BoostType=Grad:Shrinkage=$i:SeparationType=GiniIndex:nCuts=100:MinNodeSize=5:PruneMethod=NoPruning' -c 'Grad_${i}_${j}'" >> batch_submit/$filename

chmod a+xwr batch_submit/$filename

qsub -V -N "Grad_${i}_${j}_${1}_medpTV" -q medium -l mem=24gb -j oe batch_submit/$filename

done
done