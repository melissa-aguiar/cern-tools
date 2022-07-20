  # # # # # # # # # # # # # # # # # # # # # # # # # #
 #                                                   #
#   Description: Script to convert .h2000 to .npy     #
#                                                     #
#   Author: Melissa Aguiar                            #
#                                                     #
#   Created: Jul. 20, 2022                            #
 #                                                   #
  # # # # # # # # # # # # # # # # # # # # # # # # # #

import numpy as np
import ROOT

side = 4
mod = 64
cell = 8
pulse = 7

# Leitura dos dados
chain = ROOT.TChain("h2000","")
filename = "tile_0_.aan.root"

chain.Add(filename+"/h2000")

nentries = chain.GetEntries()

print(nentries)

chain.GetEntry(0)

run = getattr(chain,"Run")
evt = getattr(chain,"Evt")
evtNr = getattr(chain,"EvtNr")

aux_sample = getattr(chain,"sample")
aux_sampleTMDB = getattr(chain,"sampleTMDB")
aux_eOpt = getattr(chain,"eOpt")

sample = np.array(aux_sample).reshape(side, mod, 48, pulse)
sampleTMDB = np.array(aux_sampleTMDB).reshape(side, mod, cell, pulse)
eOpt = np.array(aux_eOpt).reshape(side, mod, 48)


for i in range(0, mod):
  print("\n", i)
  print(eOpt[0,i,0])
  print(sample[0,i,0,:])
  print(sampleTMDB[0,i,0,:])

np.save('sampleTMDB.npy',sampleTMDB)
np.save('eOpt.npy',eOpt)
