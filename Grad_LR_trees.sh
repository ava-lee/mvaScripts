#usage: source ....sh [number of jets]
#e.g. source ....sh 3
#for i in $(seq 0.1 0.05 0.25)
#for i in $(seq 0.35 0.05 0.45)
#for i in $(seq 0.55 0.05 0.7)
#for j in $(seq 300 100 800)

#for i in $(seq 0.5 0.05 0.5)
#for j in $(seq 300 200 500)

#for i in $(seq 0.35 0.05 0.45)
#for i in $(seq 0.55 0.05 0.55)
#for j in $(seq 200 200 200)

#for i in $(seq 0.3 0.05 0.3)
#for j in $(seq 800 100 800)
cd /unix/atlas3/avalee/2DMVA/
mkdir batch_submit

for i in $(seq 0.3 0.05 0.3)
do

echo "Learning rate = $i"

for j in $(seq 800 100 800)
do

echo "Trees = $j"

filename=$(echo "Grad_${i}_${j}_${1}.sh")

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

echo "RunMVATraining -d /unix/atlas3/avalee/MVA/SMU_1lep_truthtag_32-07/ -a 1 -s VH -m $1 -x $1 -l 150 -H '!H:!V:NTrees=$j:MaxDepth=4:BoostType=Grad:Shrinkage=$i:SeparationType=GiniIndex:nCuts=100:MinNodeSize=5:PruneMethod=NoPruning' -c 'Grad_${i}_${j}'" >> batch_submit/$filename

chmod a+xwr batch_submit/$filename

qsub -N "Grad_${i}_${j}_${1}" -q medium -j oe batch_submit/$filename

done
done