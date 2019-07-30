Folder Organization Example
Project folder is at a location findable by O2

(base) bionerd@MTS-LSP-L06275:~/Dana_Farber/CyCif/git/CyCif_O2_Manager/example_data$ pwd
/home/bionerd/Dana_Farber/CyCif/git/CyCif_O2_Manager/example_data
Within your data folder there are separate folders for each imaged slide

Can be whole tissue slide or TMA (eventually)
(base) bionerd@MTS-LSP-L06275:~/Dana_Farber/CyCif/git/CyCif_O2_Manager/example_data$ ll
drwxrwxrwx 1 bionerd bionerd 4096 Aug  9 08:03 image_1/
drwxrwxrwx 1 bionerd bionerd 4096 Aug  9 08:04 image_2/
each folder should contain a subfolder: 'raw_files' with
where for each CyCIF cycle there should the raw images from the microscope
for example from Rare Cycte: '.rcpnl' and '.metadata '
(base) bionerd@MTS-LSP-L06275:~/Dana_Farber/CyCif/git/CyCif_O2_Manager/example_data$ ll image_1/
total 0
drwxrwxrwx 1 bionerd bionerd 4096 Aug  9 10:44 ./
drwxrwxrwx 1 bionerd bionerd 4096 Aug  7 12:19 ../
drwxrwxrwx 1 bionerd bionerd 4096 Aug  9 08:04 raw_files/
[ntj8@login01 image_1]$ cd raw_files/
[ntj8@login01 raw_files]$ ll
total 3326644
-rwxrwx--- 1 ntj8 ntj8      11516 Jul  9 17:30 Scan_20190612_164155_01x4x00154.metadata
-rwxrwx--- 1 ntj8 ntj8 1703221248 Jul  9 17:31 Scan_20190612_164155_01x4x00154.rcpnl
-rwxrwx--- 1 ntj8 ntj8      11524 Jul  9 17:31 Scan_20190613_125815_01x4x00154.metadata
-rwxrwx--- 1 ntj8 ntj8 1703221248 Jul  9 17:32 Scan_20190613_125815_01x4x00154.rcpnl
After the CyCIF Pipeline is run there will be additional folders made (explained later), for each slide

## Requirements
                                                                                                         - Can be run either locally or on O2
- user must have O2 account
        - access to 'transfer_users' and 'ImStor_sorger' groups
        - to check:
```{bash,eval==FALSE}
groups
```
        - If lack O2 access or groups, request at "https://rc.hms.harvard.edu/"
- data follows Folder Organization (shown below)
- file 'markers.csv' that lists on each row the name of marker in order imaged
        - Example:
```{bash,eval==FALSE}
DNA1
AF488
AF555
AF647
DNA2
mLY6C
mCD8A
mCD68
DNA3
CD30
CPARP
CD7
