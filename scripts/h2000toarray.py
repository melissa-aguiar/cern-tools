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

# Select data to generate .npy files

generate_eOptTMDB   = True                # Energy [MeV] from TileCal for TMDB cells
generate_sampleTMDB = True                # Samples from TMDB
generate_sampleTile = True                # Samples from TileCal
generate_eOpt       = False               # Energy [MeV] from TileCal for all cells

# Compose path names and create folders

data_path           = "data"              # Path for the data input
user                = "msantosa"          # Username in data input files
run_number          = "429137"            # Run number of the data input
input_file_number   = "29831546"          # File number in data input files

output_path = "files/files_" + run_number # Path for the data output

os.system("mkdir files")
os.system("mkdir " + output_path)

# Configure output data

nFiles              = 40                  # Number of input files to process
packets             = 2                   # Number of data packets to generate
events_num          = 10000               # Number of events for each data packet

# Data characteristic

sides               = 4                   # Number of sides (EBA, EBC, LBA, LBC)
modules             = 64                  # Number of TileCal modules
cells_tmdb          = 8                   # Number of TMDB cells
cells_tile          = 48                  # Number of Tilecal cells
cells_in_use        = 4                   # Number of cells in use (D5R, D5L, D6R, D6L)
pulses              = 7                   # Number of samples for each pulse

cells_map = {0: 17, 1: 16, 2: 37, 3: 38}  # Mapping cells from TMDB to Tilecal
sides_map = {3:'EBA',2:'EBC'}             # Mapping sides for TMDB

chain = ROOT.TChain("h2000","")

for i in tqdm(range(1, nFiles+1), desc="Loading files"):
  filename = data_path + "/user." + user + "." + input_file_number + ".AANT._" + f"{i:06}" + ".root"
  chain.Add(filename+"/h2000")

nentries = chain.GetEntries()

if events_num < chain.GetEntries():
  nentries = events_num
else:
  print("Error!")
  print("Number of events selected > Total events")
  exit()

print("Number of events: " + str(nentries*packets))

for pack in range(0, packets):
  sampleTMDB = []
  sample = []
  eOpt = []
  eOptTMDB = np.zeros((nentries, sides, modules, cells_in_use))
  sampleTile = np.zeros((nentries, sides, modules, cells_in_use, pulses))

  desc_str = "Processing packets " + "[" + str(pack+1) + "/" + str(packets) + "]"
  for evt in tqdm(range(0,nentries), desc=desc_str):
    chain.GetEntry(events_num*pack + evt)
    aux_sampleTMDB = getattr(chain,"sampleTMDB")
    aux_sample = getattr(chain,"sample")
    aux_eOpt = getattr(chain,"eOpt")
    sampleTMDB.append(np.array(aux_sampleTMDB).reshape(sides, modules, cells_tmdb, pulses))
    sample.append(np.array(aux_sample).reshape(sides, modules, cells_tile, pulses))
    eOpt.append(np.array(aux_eOpt).reshape(sides, modules, cells_tile))

    for sd in sides_map:
      for md in range(0, modules):
        for ch in cells_map:
          eOptTMDB[evt][sd][md][ch] = np.array(eOpt[evt][sd][md][cells_map.get(ch)])
          sampleTile[evt][sd][md][ch][:] = np.array(sample[evt][sd][md][cells_map.get(ch)][:])

  print("Saving output files...")

  if generate_sampleTMDB:
    np.save(output_path + '/sampleTMDB' + '_' + run_number + '_' + str(pack) + '.npy', sampleTMDB)

  if generate_eOptTMDB:
    np.save(output_path + '/eOptTMDB' + '_' + run_number + '_' + str(pack) + '.npy', eOptTMDB)

  if generate_sampleTile:
    np.save(output_path + '/sampleTile' + '_' + run_number + '_' + str(pack) + '.npy', sampleTile)

  if generate_eOpt:
    np.save(output_path + '/eOpt' + '_' + run_number + '_' + str(pack) + '.npy', eOpt)

  print("Done!")
