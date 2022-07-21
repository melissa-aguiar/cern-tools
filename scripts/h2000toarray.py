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
import os

sides = 4
modules = 64
cells_tmdb = 8
cells_atlas = 48
pulses = 7

nFiles = 40

choose_events_num = False
events_num = 1000

user = "pbragali"
run_number = "29676563"
data_path = "data"
output_path = "files/files_" + run_number

os.system("mkdir " + output_path)

# Leitura dos dados
chain = ROOT.TChain("h2000","")

for i in range(1, nFiles+1):
  filename = data_path + "/user." + user + "." + run_number + ".AANT._" + f"{i:06}" + ".root"
  chain.Add(filename+"/h2000")

nentries = chain.GetEntries()

if choose_events_num:
  if events_num < chain.GetEntries():
    nentries = events_num

sampleTMDB = []
eOpt = []

for entryNum in range(0,nentries):

  print("Processing event %d of %d..."%(entryNum+1, nentries))
  chain.GetEntry(entryNum)

  aux_sampleTMDB = getattr(chain,"sampleTMDB")
  aux_eOpt = getattr(chain,"eOpt")

  sampleTMDB.append(np.array(aux_sampleTMDB).reshape(sides, modules, cells_tmdb, pulses))
  eOpt.append(np.array(aux_eOpt).reshape(sides, modules, cells_atlas))

print("Saving output files...")
np.save(output_path + '/sampleTMDB' + '_' + run_number + '.npy', sampleTMDB)
np.save(output_path + '/eOpt' + '_' + run_number + '.npy', eOpt)
print("Done!")
