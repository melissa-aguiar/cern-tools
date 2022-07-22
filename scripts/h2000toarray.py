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

channel = {0: 17, 1: 16, 2: 37, 3: 38}
sideTMDB = {3:'EBA',2:'EBC'}

nFiles = 40

choose_events_num = True
events_num = 50000
packets = 5

user = "pbragali"
run_number = "29676563"
data_path = "data"
output_path = "files/files_" + run_number

os.system("mkdir files")
os.system("mkdir " + output_path)

chain = ROOT.TChain("h2000","")

for i in range(1, nFiles+1):
  filename = data_path + "/user." + user + "." + run_number + ".AANT._" + f"{i:06}" + ".root"
  chain.Add(filename+"/h2000")

nentries = chain.GetEntries()

if choose_events_num:
  if events_num < chain.GetEntries():
    nentries = events_num
  else:
    print("Error!")
    print("Number of events selected > Total events")
    exit()

  for pack in range(0, packets):
    sampleTMDB = []
    eOpt = []
    eOptTMDB = np.zeros((nentries, sides, modules, cells_energy))
    desc_str = "Processing events" + "[" + str(pack+1) + "/" + str(packets) + "]"
    for evt in tqdm(range(0,nentries), desc=desc_str):
      chain.GetEntry(events_num*pack + evt)
      aux_sampleTMDB = getattr(chain,"sampleTMDB")
      aux_eOpt = getattr(chain,"eOpt")
      sampleTMDB.append(np.array(aux_sampleTMDB).reshape(sides, modules, cells_tmdb, pulses))
      eOpt.append(np.array(aux_eOpt).reshape(sides, modules, cells_atlas))

      for sd in sideTMDB:
        for md in range(0, modules):
          for ch in channel:
            eOptTMDB[evt][sd][md][ch] = np.array(eOpt[evt][sd][md][channel.get(ch)])

    print("Saving output files...")
    np.save(output_path + '/sampleTMDB' + '_' + run_number + '_' + str(pack) + '.npy', sampleTMDB)
    np.save(output_path + '/eOptTMDB' + '_' + run_number + '_' + str(pack) + '.npy', eOptTMDB)
    print("Done!")

else:
  sampleTMDB = []
  eOpt = []
  eOptTMDB = np.zeros((nentries, sides, modules, cells_energy))

  for evt in tqdm(range(0,nentries), desc="Processing events"):
    chain.GetEntry(evt)
    aux_sampleTMDB = getattr(chain,"sampleTMDB")
    aux_eOpt = getattr(chain,"eOpt")
    sampleTMDB.append(np.array(aux_sampleTMDB).reshape(sides, modules, cells_tmdb, pulses))
    eOpt.append(np.array(aux_eOpt).reshape(sides, modules, cells_atlas))

    for sd in sideTMDB:
      for md in range(0, modules):
        for ch in channel:
          eOptTMDB[evt][sd][md][ch] = np.array(eOpt[evt][sd][md][channel.get(ch)])

  print("Saving output files...")
  np.save(output_path + '/sampleTMDB' + '_' + run_number + '.npy', sampleTMDB)
  np.save(output_path + '/eOptTMDB' + '_' + run_number + '.npy', eOptTMDB)
  print("Done!")
