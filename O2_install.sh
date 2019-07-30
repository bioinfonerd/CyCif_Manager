#!/bin/bash

#attach pipeline to bash path
echo 'CYCIF=/n/groups/lsp/cycif/CyCif_Manager/O2:/n/groups/lsp/cycif/CyCif_Manager/bin' >> ~/.bash_profile
echo 'export PATH=$CYCIF:$PATH' >> ~/.bash_profile

#reload current environment 
source ~/.bash_profile
