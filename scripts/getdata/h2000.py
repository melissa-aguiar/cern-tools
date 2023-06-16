#RUN2=True
RUN3=True
UDP4=True
#CondDbTag = 'CONDBR2-BLKPA-RUN2-09'
RunNumber=0
FileName='data23_900GeV.RAW.data'
#FileName='/eos/atlas/atlastier0/rucio/data22_13p6TeV/physics_Main/00431371/data22_13p6TeV.00431371.physics_Main.daq.RAW/data22_13p6TeV.00431371.physics_Main.daq.RAW._lb0221._SFO-12._0001.data'
OutputDirectory='.'

#from RecExConfig.RecFlags import rec 
#rec.doLArg = True
#includeLAr = True

doTileNtuple=True

doCaloNtuple=False
doTileMon=False
doTileCalib=False

doTileOpt2=True
doTileOpt1=False
doTileOptATLAS=False
doTileFit=False
doAtlantis=False
TileUseDCS=False

useRODReco=False
useTMDB=True

include("TileRecEx/jobOptions_TileCalibRec.py")

topSequence.TileNtuple.BSInput = True
