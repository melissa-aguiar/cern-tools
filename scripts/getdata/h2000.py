
from RecExConfig.RecFlags import rec

RunNumber       = 0
RUN2            = False
RUN3            = True
UDP4            = True
useTMDB         = True
doTileNtuple    = True
doTileOpt2      = True
doTileOpt1      = False
rec.doLArg      = False
includeLAr      = False
doCaloNtuple    = False
doTileMon       = False
doTileCalib     = False
doTileOptATLAS  = False
doTileFit       = False
doAtlantis      = False
TileUseDCS      = False
useRODReco      = False

FileName        = '/eos/atlas/atlastier0/rucio/data22_13p6TeV/physics_Main/00427394/data22_13p6TeV.00427394.physics_Main.daq.RAW/data22_13p6TeV.00427394.physics_Main.daq.RAW._lb0221._SFO-12._0001.data'
OutputDirectory = '.'
#CondDbTag      = 'CONDBR2-BLKPA-RUN2-09'

include("TileRecEx/jobOptions_TileCalibRec.py")

topSequence.TileNtuple.BSInput         = False
svcMgr.EventSelector.Input             = []
svcMgr.ByteStreamInputSvc.FullFileName = [ FileName ]
