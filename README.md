## Instructions to Configure Environment


Acess LxPlus using your cern username and password:

    ssh -XY {cern-username}@lxplus.cern.ch

Setup ATLAS environment:

    setupATLAS

Setup CERN's Grid [*]:

    voms-proxy-init -voms atlas

Configure Athena v23:

    asetup Athena,23.0.0

Setup Rucio:

    lsetup rucio

Configure Athena v22:

    asetup Athena,22.0.0

Setup Panda:

    lsetup panda


[*] To get acess to CERN's Grid, get a digital certificate and join ATLAS Virtual Organization following the links:

    https://twiki.cern.ch/twiki/bin/viewauth/AtlasComputing/WorkBookStartingGrid

    https://atlassoftwaredocs.web.cern.ch/ASWTutorial/basicSetup/grid_vo/

## Instructions to Get Run Data


Clone the repository (HTTPS):

    git clone https://github.com/melissa-aguiar/cern-tools.git

Clone the repository (SSH):

    git clone git@github.com:melissa-aguiar/cern-tools.git

Go to getdata folder:

    cd cern-tools/scripts/getdata
    
Go to ATLAS Run Query and select the desired run number:

    https://atlas-runquery.cern.ch/

List files for run 427892:

    rucio list-dids data22_13p6TeV:data22_13p6TeV*427892*.RAW

List files for Physics Main data from run 427892:

    rucio list-files data22_13p6TeV.00427892.physics_Main.daq.RAW

Use CERN's Grid to download Physics Main data from run 427892:

    source panda.sh data22_13p6TeV.00427892.physics_Main.daq.RAW

If the task is running, we will have a TaskID and a SUCCESS message in the file job.tmp:

    cat job.tmp

The task can be monitored in BigPanda:

    https://bigpanda.cern.ch/user/

When the task is done, go to the task page and get the containers name (OUTPUT0) and download it:

(The download files will be stored in the current path)

    rucio download user.{cern-username}.data22_13p6TeV.00427892.physics_Main.daq.RAW.h2000.v1_AANT.440329476
