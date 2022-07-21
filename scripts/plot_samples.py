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
import matplotlib.pyplot as plt

# Plot all events for each cell

mod = range(0, 64)
side = {3:'EBA',2:'EBC'}
channel_str = {0: 'D5L', 1:'D5R', 2:'D6L', 3:'D6R'}
channel = {0: 17, 1:16, 2:37, 3:38}


sampleTMDB = np.load('sampleTMDB.npy')
eOpt = np.load('eOpt.npy')

nentries = np.size(sampleTMDB, 0)

for sd in side:
  for md in mod:
    for ch in channel:
      for evt in range(0, nentries):
        if (eOpt[evt, sd, md, channel.get(ch)] > 2000) and (eOpt[evt, sd, md, channel.get(ch)] < 5000):
          print(side.get(sd) + f"{md:02}" + "-" + channel_str.get(ch))
          print("Evento %d de %d..."%(evt+1, nentries))
          plt.plot(sampleTMDB[evt, sd, md, ch,:])
      plt.title(side.get(sd) + f"{md:02}" + "-" + channel_str.get(ch))
      plt.savefig("plots/" + side.get(sd) + f"{md:02}" + channel_str.get(ch) + ".png")
      plt.close()

## corte de energia limite inferior e superior
