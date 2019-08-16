#!/bin/bash
jid1=$(sbatch --parsable sticher.sh)
jid2=$(sbatch --dependency=afterok:$jid1 --parsable prob_mapper.sh)
jid3=$(sbatch --dependency=afterok:$jid2 --parsable segmenter.sh)
jid4=$(sbatch --dependency=afterok:$jid3 --parsable feature_extractor.sh)
