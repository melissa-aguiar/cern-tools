  # # # # # # # # # # # # # # # # # # # # # # # # # #
 #                                                   #
#   Description: Script to plot histogram from .npy   #
#                                                     #
#   Author: Melissa Aguiar                            #
#                                                     #
#   Created: Jul. 21, 2022                            #
 #                                                   #
  # # # # # # # # # # # # # # # # # # # # # # # # # #

import numpy as np
import os
import matplotlib.pyplot as plt

# Plot all events for each cell

mod = range(0, 64)
side = {3:'EBA',2:'EBC'}
channel_str = {0: 'D5L', 1:'D5R', 2:'D6L', 3:'D6R'}
channel = {0: 17, 1:16, 2:37, 3:38}

run_number = "29676563"
input_path = "files/files_" + run_number
output_path = "plots/histogram_" + run_number

choose_energy_limits = False
limit_min = 2000
limit_max = 5000

os.system("mkdir " + output_path)

sampleTMDB = np.load(input_path + '/sampleTMDB' + '_' + run_number + '.npy')
eOpt = np.load(input_path + '/eOpt' + '_' + run_number + '.npy')

nentries = np.size(sampleTMDB, 0)
hist_data = np.zeros(nentries)

for sd in side:
  for md in mod:
    for ch in channel:
      print("Processing " + side.get(sd) + f"{md:02}" + "-" + channel_str.get(ch) + "...")
      plt.figure()
      plt.title(side.get(sd) + f"{md:02}" + "-" + channel_str.get(ch))
      for evt in range(0, nentries):
        if choose_energy_limits:
          if (eOpt[evt, sd, md, channel.get(ch)] > limit_min) and (eOpt[evt, sd, md, channel.get(ch)] < limit_max):
            pulses = sampleTMDB[evt, sd, md, ch,:]
            aux = np.where(pulses==np.max(pulses))
            hist_data[evt] = aux[0][0]
        else:
          pulses = sampleTMDB[evt, sd, md, ch,:]
          aux = np.where(pulses==np.max(pulses))
          hist_data[evt] = aux[0][0]
      plt.hist(hist_data, bins=7)
      plt.savefig(output_path + "/" + side.get(sd) + f"{md:02}" + channel_str.get(ch) + "_hist.png")
      plt.close()

