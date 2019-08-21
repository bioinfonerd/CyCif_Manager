module load conda2/4.2.13
source activate /n/groups/lsp/cycif/cycif_pipeline/
python CyCif_Pipeline_O2_v1.py $1
conda deactivate
