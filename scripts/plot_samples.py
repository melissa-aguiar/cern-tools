  # # # # # # # # # # # # # # # # # # # # # # # # # #
 #                                                   #
#   Description: Script to plot samples from .npy     #
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


mod = 64
side = {3:'EBA',2:'EBC'}
channel = {0: 'D5L', 1:'D5R', 2:'D6L', 3:'D6R'}

run_number = "429137"
input_path = "files/files_" + run_number
output_path_TMDB = "plots/samplesTMDB_" + run_number
output_path_Tile = "plots/samplesTile_" + run_number

plot_sampleTMDB = True
plot_sampleTile = True

choose_energy_limits = True
limit_min = 2000
limit_max = 5000

os.system("mkdir plots")

packets = 2

sampleTMDB = []
sampleTile = []
eOpt = []

for pack in tqdm(range(0, packets), desc="Loading files"):
  sampleTMDB.append(np.load(input_path + '/sampleTMDB' + '_' + run_number+ '_' + str(pack) + '.npy'))
  sampleTile.append(np.load(input_path + '/sampleTile' + '_' + run_number+ '_' + str(pack) + '.npy'))
  eOpt.append(np.load(input_path + '/eOptTMDB' + '_' + run_number + '_' + str(pack) + '.npy'))


if plot_sampleTMDB:
  os.system("mkdir " + output_path_TMDB)
  print("############# Plot TMDB Samples #############")
  nentries = np.size(sampleTMDB, 1)
  print("Number of entries: " + str(nentries*packets))

  for sd in side:
    for md in tqdm(range(0, mod), desc="Processing " + side.get(sd)):
      for ch in channel:
        cnt = 0
        for evt in range(0, nentries):
          if choose_energy_limits:
            for pack in range(0, packets):
              if (eOpt[pack][evt][sd][md][ch] > limit_min) and (eOpt[pack][evt][sd][md][ch] < limit_max):
                plt.plot(range(1, 8), sampleTMDB[pack][evt][sd][md][ch][:])
                cnt = cnt + 1
          else:
            for pack in range(0, packets):
              plt.plot(range(1, 8), sampleTMDB[pack][evt][sd][md][ch][:])
            cnt = cnt + 1
        plt.title(side.get(sd) + f"{md+1:02}" + "-" + channel.get(ch) + " | Number of events: " + str(cnt))
        plt.xlabel("TMDB Sample")
        plt.ylabel("Amplitude [ADC]")
        plt.savefig(output_path_TMDB + "/" + side.get(sd) + f"{md+1:02}" + channel.get(ch) + ".png")
        plt.close()

if plot_sampleTile:
  os.system("mkdir " + output_path_Tile)
  print("############# Plot Tile Samples #############")
  nentries = np.size(sampleTile, 1)
  print("Number of entries: " + str(nentries*packets))

  for sd in side:
    for md in tqdm(range(0, mod), desc="Processing " + side.get(sd)):
      for ch in channel:
        cnt = 0
        for evt in range(0, nentries):
          if choose_energy_limits:
            for pack in range(0, packets):
              if (eOpt[pack][evt][sd][md][ch] > limit_min) and (eOpt[pack][evt][sd][md][ch] < limit_max):
                plt.plot(range(1, 8), sampleTile[pack][evt][sd][md][ch][:])
                cnt = cnt + 1
          else:
            for pack in range(0, packets):
              plt.plot(range(1, 8), sampleTile[pack][evt][sd][md][ch][:])
            cnt = cnt + 1
        plt.title(side.get(sd) + f"{md+1:02}" + "-" + channel.get(ch) + " | Number of events: " + str(cnt))
        plt.xlabel("Tile Sample")
        plt.ylabel("Amplitude [ADC]")
        plt.savefig(output_path_Tile + "/" + side.get(sd) + f"{md+1:02}" + channel.get(ch) + ".png")
        plt.close()
