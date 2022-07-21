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
cells = 48
pulse = 7

nFiles = 6

eventLim = False
numEvts = 1000

# Leitura dos dados
chain = ROOT.TChain("h2000","")
for i in range(1, nFiles+1):
  filename = "data/user.pbragali.29676563.AANT._" + f"{i:06}" + ".root"
  chain.Add(filename+"/h2000")

if eventLim:
  if numEvts < chain.GetEntries():
    nentries = numEvts
  else:
    nentries = chain.GetEntries()
else:
  nentries   = chain.GetEntries()

print("Total de eventos: ", nentries)

sampleTMDB = []
eOpt = []

for entryNum in range(0,nentries):

  chain.GetEntry(entryNum)

  aux_sampleTMDB = getattr(chain,"sampleTMDB")
  aux_eOpt = getattr(chain,"eOpt")

  sampleTMDB.append(np.array(aux_sampleTMDB).reshape(side, mod, cell, pulse))
  eOpt.append(np.array(aux_eOpt).reshape(side, mod, cells))

np.save('sampleTMDB.npy', sampleTMDB)
np.save('eOpt.npy', eOpt)
