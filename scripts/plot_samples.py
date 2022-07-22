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

# Plot all events for each cell

mod = 64
side = {3:'EBA',2:'EBC'}
channel = {0: 'D5L', 1:'D5R', 2:'D6L', 3:'D6R'}

run_number = "29676563"
input_path = "files/files_" + run_number
output_path = "plots/samples_" + run_number

choose_energy_limits = True
limit_min = 2000
limit_max = 5000

os.system("mkdir plots")
os.system("mkdir " + output_path)

events_pack = True
packets = 5

if events_pack:
  sampleTMDB = []
  eOpt = []
  print("Loading files...")
  for pack in range(0, packets):
    sampleTMDB.append(np.load(input_path + '/sampleTMDB' + '_' + run_number+ '_' + str(pack) + '.npy'))
    eOpt.append(np.load(input_path + '/eOptTMDB' + '_' + run_number + '_' + str(pack) + '.npy'))
  print("Done!")
  nentries = np.size(sampleTMDB, 1)

  for sd in side:
    for md in range(0, mod):
      print("Processing " + side.get(sd) + f"{md+1:02}" + "...")
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
        plt.xlabel("Sample")
        plt.ylabel("Amplitude [ADC]")
        plt.savefig(output_path + "/" + side.get(sd) + f"{md+1:02}" + channel.get(ch) + ".png")
        plt.close()



else:
  sampleTMDB = np.load(input_path + '/sampleTMDB' + '_' + run_number + '.npy')
  eOpt = np.load(input_path + '/eOptTMDB' + '_' + run_number + '.npy')

  nentries = np.size(sampleTMDB, 0)

  for sd in side:
    for md in range(0, mod):
      print("Processing " + side.get(sd) + f"{md+1:02}" + "...")
      for ch in channel:
        cnt = 0
        for evt in range(0, nentries):
          if choose_energy_limits:
            if (eOpt[evt, sd, md, ch] > limit_min) and (eOpt[evt, sd, md, ch] < limit_max):
              plt.plot(range(1, 8), sampleTMDB[evt, sd, md, ch,:])
              cnt = cnt + 1
          else:
            plt.plot(range(1, 8), sampleTMDB[evt, sd, md, ch,:])
            cnt = cnt + 1
        plt.title(side.get(sd) + f"{md+1:02}" + "-" + channel.get(ch) + " | Number of events: " + str(cnt))
        plt.xlabel("Sample")
        plt.ylabel("Amplitude [ADC]")
        plt.savefig(output_path + "/" + side.get(sd) + f"{md+1:02}" + channel.get(ch) + ".png")
        plt.close()

