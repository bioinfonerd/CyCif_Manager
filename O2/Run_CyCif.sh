#!/bin/bash
jid1=$(sbatch --parsable transfer_from.sh)
jid2=$(sbatch --dependency=afterok:$jid1 --parsable QC.sh)
jid3=$(sbatch --dependency=afterok:$jid2 --parsable illumination.sh)
jid4=$(sbatch --dependency=afterok:$jid3 --parsable stitcher.sh)
jid5=$(sbatch --dependency=afterok:$jid4 --parsable prob_mapper.sh)
jid6=$(sbatch --dependency=afterok:$jid5 --parsable segmenter.sh)
jid7=$(sbatch --dependency=afterok:$jid6 --parsable feature_extractor.sh)
jid8=$(sbatch --dependency=afterok:$jid7 --parsable transfer_to.sh)
