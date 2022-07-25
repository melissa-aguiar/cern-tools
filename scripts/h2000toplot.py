  # # # # # # # # # # # # # # # # # # # # # # # # # #
 #                                                   #
#   Description: Script to plot samples from h2000    #
#                                                     #
#   Author: Melissa Aguiar                            #
#                                                     #
#   Created: Jul. 21, 2022                            #
 #                                                   #
  # # # # # # # # # # # # # # # # # # # # # # # # # #

import numpy as np
import ROOT
import os
import matplotlib.pyplot as plt
from tqdm import tqdm

sides = 4
modules = 64
cells_tmdb = 8
cells_atlas = 48
cells_energy = 4
pulses = 7

channel = {0: 17, 1: 16, 2: 37, 3: 38}
channel_str = {0: 'D5L', 1:'D5R', 2:'D6L', 3:'D6R'}
sideTMDB = {3:'EBA',2:'EBC'}

nFiles = 291

choose_events_num = True
events_num = 100000
packets = 10

user = "pbragali"
run_number = "29676563"
data_path = "cernbox"
input_path = "files/files_" + run_number
output_path = "plots/samples_" + run_number + "_" + str(packets*events_num) + "evts"

limit_min = 2000
limit_max = 5000

os.system("mkdir plots")
os.system("mkdir " + output_path)

chain = ROOT.TChain("h2000","")

print("Loading files...")

for i in tqdm(range(1, nFiles+1), desc="Loading files"):
  if i != 120:
    filename = data_path + "/user." + user + "." + run_number + ".AANT._" + f"{i:06}" + ".root"
    chain.Add(filename+"/h2000")

print("Done!")

nentries = chain.GetEntries()
print(nentries)
exit()

if choose_events_num:
  if events_num < chain.GetEntries():
    nentries = events_num
  else:
    print("Error!")
    print("Number of events selected > Total events")
    exit()

eOptTMDB = np.zeros((packets,nentries, sides, modules, cells_energy))
sampleTMDB = np.zeros((packets,nentries, sides, modules, cells_energy, pulses))

for pack in range(0, packets):
  auxsampleTMDB = []
  eOpt = []
  desc_str = "Processing packets " + "[" + str(pack+1) + "/" + str(packets) + "]"
  for evt in tqdm(range(0,nentries), desc=desc_str):
    chain.GetEntry(events_num*pack + evt)
    aux_sampleTMDB = getattr(chain,"sampleTMDB")
    aux_eOpt = getattr(chain,"eOpt")
    auxsampleTMDB.append(np.array(aux_sampleTMDB).reshape(sides, modules, cells_tmdb, pulses))
    eOpt.append(np.array(aux_eOpt).reshape(sides, modules, cells_atlas))

    for sd in sideTMDB:
      for md in range(0, modules):
        for ch in channel:
          eOptTMDB[pack][evt][sd][md][ch] = np.array(eOpt[evt][sd][md][channel.get(ch)])
          sampleTMDB[pack][evt][sd][md][ch][:] = np.array(auxsampleTMDB[evt][sd][md][ch][:])

for sd in sideTMDB:
  for md in tqdm(range(0, modules), desc="Processing " + sideTMDB.get(sd)):
    for ch in channel:
      cnt = 0
      for evt in range(0, nentries):
        for pack in range(0, packets):
          if (eOptTMDB[pack][evt][sd][md][ch] > limit_min) and (eOptTMDB[pack][evt][sd][md][ch] < limit_max):
            plt.plot(range(1, 8), sampleTMDB[pack][evt][sd][md][ch][:])
            cnt = cnt + 1
      plt.title(sideTMDB.get(sd) + f"{md+1:02}" + "-" + channel_str.get(ch) + " | Number of events: " + str(cnt))
      plt.xlabel("Sample")
      plt.ylabel("ADC")
      plt.savefig(output_path + "/" + sideTMDB.get(sd) + f"{md+1:02}" + channel_str.get(ch) + ".png")
      plt.close()
