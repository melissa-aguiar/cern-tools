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
from tqdm import tqdm

sides = 4
modules = 64
cells_tmdb = 8
cells_atlas = 48
cells_energy = 4
pulses = 7

nFiles = 40

choose_energy_limits = False
limit_min = 2000
limit_max = 5000

choose_events_num = True
events_num = 150000

user = "pbragali"
run_number = "29676563"
data_path = "data"
output_path = "files/files_" + run_number

os.system("mkdir files")
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
eOptTMDB = np.zeros((nentries, sides, modules, cells_energy))
muonTMDB = np.zeros((nentries, sides, modules, cells_energy, pulses))

for evt in tqdm(range(0,nentries), desc="Processing events"):
  chain.GetEntry(evt)

  aux_sampleTMDB = getattr(chain,"sampleTMDB")
  aux_eOpt = getattr(chain,"eOpt")

  sampleTMDB.append(np.array(aux_sampleTMDB).reshape(sides, modules, cells_tmdb, pulses))
  eOpt.append(np.array(aux_eOpt).reshape(sides, modules, cells_atlas))

  for sd in range(0, sides):
    for md in range(0, modules):
      eOptTMDB[evt][sd][md][0] = np.array(eOpt[evt][sd][md][17])
      eOptTMDB[evt][sd][md][1] = np.array(eOpt[evt][sd][md][16])
      eOptTMDB[evt][sd][md][2] = np.array(eOpt[evt][sd][md][37])
      eOptTMDB[evt][sd][md][3] = np.array(eOpt[evt][sd][md][38])

if choose_energy_limits:
  for evt in tqdm(range(0, nentries), desc="Selecting samples"):
    for sd in range(0, sides):
      for md in range(0, modules):
        for ch in range(0, cells_energy):
          if (eOptTMDB[evt][sd][md][ch] > limit_min) and (eOptTMDB[evt, sd, md, ch] < limit_max):
            muonTMDB[evt][sd][md][ch][:] = np.array(sampleTMDB[evt][sd][md][ch][:])
  print("Saving output files...")
  np.save(output_path + '/muonTMDB' + '_' + run_number + '.npy', muonTMDB)
  print("Done!")
else:
  print("Saving output files...")
  np.save(output_path + '/sampleTMDB' + '_' + run_number + '.npy', sampleTMDB)
  np.save(output_path + '/eOptTMDB' + '_' + run_number + '.npy', eOptTMDB)
  print("Done!")



