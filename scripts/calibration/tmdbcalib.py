
print('         # # # # # # # # # # # # # # # # # # # # # # # # # #')
print('        #                                                   #')
print('       #   Description: Script to calibrate TMDB boards      #')
print('       #                                                     #')
print('       #                                                     #')
print('       #   Created: Aug. 05, 2022                            #')
print('        #                                                   #')
print('         # # # # # # # # # # # # # # # # # # # # # # # # # #\n')

print(">> Importing libraries and defining funcions...")

import os
import matplotlib.pyplot      as plt
import seaborn                as sns
import numpy                  as np
from   sklearn.covariance import MinCovDet
from   tqdm               import tqdm

import warnings
warnings.filterwarnings('ignore')

def robust_cov(A):
    """
    Returns the robust estimator of the covariance for matrix A

    """

    robust_cov = MinCovDet().fit(A.T).covariance_

    return robust_cov

print(">> Importing libraries and defining funcions... Done!\n")

print(">> Loading data...")

run_number = "429137"
input_path = "../../files/"
plots_path = "../../plots/plots_" + run_number

sampleZB   = np.concatenate((np.load(input_path + 'sampleZB_427892_0.npy'), np.load(input_path + 'sampleZB_427892_1.npy')), axis=0)
sampleMuon = np.load(input_path + '/sampleMuon' + '_' + run_number + '.npy')
eOptMuon   = np.load(input_path + '/eOptMuon'   + '_' + run_number + '.npy')

print("SampleZB shape:   ",   sampleZB.shape)
print("SampleMuon shape: ", sampleMuon.shape)
print("eOptMuon shape:   ",   eOptMuon.shape)

print(">> Loading data... Done!\n")

print(">> Declare variables and create folders...")

sides        = 4                                     # Number of sides (EBA, EBC, LBA, LBC)
modules      = 64                                    # Number of TileCal modules
cells_tmdb   = 8                                     # Number of TMDB cells
cells_tile   = 48                                    # Number of Tilecal cells
cells_in_use = 4                                     # Number of cells in use (D5R, D5L, D6R, D6L)
pulses       = 7                                     # Number of samples for each pulse
pulses_axis  = range(1, 8)                           # Axis for plotting pulses

limit_min    = 600                                   # Minimum energy limit [MeV]
limit_max    = 5000                                  # Maximum energy limit [MeV]
entries      = 50000                                 # Number of entries to process
threshold    = 500                                   # Energy value [MeV] to fit with quantized sample

cells_map    = {0: 17, 1: 16, 2: 37, 3: 38}          # Mapping cells from TMDB to Tilecal
channel      = {0: 'D5L', 1:'D5R', 2:'D6L', 3:'D6R'} # Channels name
sides_map    = {2:'EBA', 3:'EBC'}                    # Mapping sides for TMDB
events_map   = range(0, np.size(sampleMuon, 0))      # Mapping events
pulses_map   = range(0, pulses)                      # Mapping pulses
mods_map     = np.range(0, modules)                  # Mapping modules

samples_ped  = np.zeros((np.size(sampleMuon, 0), sides, modules, cells_in_use, pulses))

C            = np.zeros((sides, modules, cells_in_use, pulses, pulses))
C_inv        = np.zeros((sides, modules, cells_in_use, pulses, pulses))

mean_pulse   = np.zeros((sides, modules, cells_in_use, pulses))
norm_pulse   = np.zeros((sides, modules, cells_in_use, pulses))
pedestal     = np.zeros((sides, modules, cells_in_use, pulses))
w            = np.zeros((sides, modules, cells_in_use, pulses))
quant_w      = np.zeros((sides, modules, cells_in_use, pulses))

old_std      = np.zeros((sides, modules,               7)) # D5R, D5L, D6R, D6L, D5, D6 and D5+D6
new_std      = np.zeros((sides, modules,               7)) # D5R, D5L, D6R, D6L, D5, D6 and D5+D6
std_relat    = np.zeros((sides, modules,               7)) # D5R, D5L, D6R, D6L, D5, D6 and D5+D6
e500         = np.zeros((sides, modules, cells_in_use, 1))

os.system("mkdir ../../data")
os.system("mkdir ../../data/data_" + run_number)

os.system("mkdir ../../plots")
os.system("mkdir " + plots_path)
os.system("mkdir " + plots_path +     "/all_modules")
os.system("mkdir " + plots_path +        "/pedestal")
os.system("mkdir " + plots_path +      "/covariance")
os.system("mkdir " + plots_path +  "/covariance_inv")
os.system("mkdir " + plots_path +          "/filter")
os.system("mkdir " + plots_path +             "/fit")
os.system("mkdir " + plots_path +      "/mean_pulse")
os.system("mkdir " + plots_path + "/mean_pulse_norm")
os.system("mkdir " + plots_path +         "/samples")
os.system("mkdir " + plots_path +         "/weights")

for sd in sides_map:
    for md in mods_map:
        os.system("mkdir " + plots_path + "/all_modules/" + sides_map.get(sd) + f"{md+1:02}")

print(">> Declare variables and create folders... Done!\n")

print(">> Calculate pedestal and mean pulses...")

for sd in sides_map:
    for md in mods_map:
        for ch in cells_map:
            for i in pulses_map:
                pedestal[sd, md, ch, i] = np.mean(sampleZB[:, sd, md, ch, i])

for evt in events_map:
    for sd in sides_map:
        for md in mods_map:
            for ch in cells_map:
                samples_ped[evt,sd,md,ch,:] = sampleMuon[evt,sd,md,ch,:] - pedestal[sd, md, ch, :]
                for i in pulses_map:
                    mean_pulse[sd,md,ch,i]  = np.mean([mean_pulse[sd,md,ch,i], samples_ped[evt,sd,md,ch,i]])

for sd in sides_map:
    for md in mods_map:
        for ch in cells_map:
            for i in pulses_map:
                norm_pulse[sd,md,ch,i] = mean_pulse[sd,md,ch,i]/np.max(mean_pulse[sd,md,ch,:])

print(">> Calculate pedestal and mean pulses... Done!\n")

print(">> Plot pedestal, samples and mean pulses...")

for sd in sides_map:
    for md in mods_map:
        plt.figure(figsize = (20, 12))
        for ch in cells_map:
            plt.subplot(2,2,ch+1)
            plt.grid()
            plt.plot(pulses_axis, pedestal[sd, md, ch, :], '-x')
            plt.title("Pedestal | " + sides_map.get(sd) + f"{md+1:02}" + " - " + channel.get(ch))
            plt.xlabel("Sample")
            plt.ylabel("Amplitude [ADC]")
        output_path = plots_path + "/all_modules/" + sides_map.get(sd) + f"{md+1:02}"
        plt.savefig(output_path  + "/"             + sides_map.get(sd) + f"{md+1:02}" + "_pedestal.jpeg")
        plt.savefig(plots_path   + "/pedestal/"    + sides_map.get(sd) + f"{md+1:02}" + "_pedestal.jpeg")
        plt.close()

for sd in sides_map:
    for md in mods_map:
        plt.figure(figsize = (20, 12))
        for ch in cells_map:
            for i in range(0, np.size(samples_ped, 0)):
                plt.subplot(2,2,ch+1)
                plt.plot(pulses_axis, samples_ped[i,sd, md, ch, :])
            plt.title("Muon samples without pedestal | " + sides_map.get(sd) + f"{md+1:02}" + " - " + channel.get(ch) + " | Number of events: " + str(np.size(samples_ped, 0)))
            plt.xlabel("Sample")
            plt.ylabel("Amplitude [ADC]")
            plt.grid()
        output_path = plots_path + "/all_modules/" + sides_map.get(sd) + f"{md+1:02}"
        plt.savefig(output_path  + "/"             + sides_map.get(sd) + f"{md+1:02}" + "_samples.jpeg")
        plt.savefig(plots_path   + "/samples/"     + sides_map.get(sd) + f"{md+1:02}" + "_samples.jpeg")
        plt.close()

for sd in sides_map:
    for md in mods_map:
        plt.figure(figsize = (20, 12))
        for ch in cells_map:
            plt.subplot(2,2,ch+1)
            plt.plot(pulses_axis, mean_pulse[sd,md,ch,:])
            plt.title("Mean pulse | " + sides_map.get(sd) + f"{md+1:02}" + " - " + channel.get(ch))
            plt.xlabel("Sample")
            plt.ylabel("Amplitude [ADC]")
            plt.grid()
        output_path = plots_path + "/all_modules/" + sides_map.get(sd) + f"{md+1:02}"
        plt.savefig(output_path  + "/"             + sides_map.get(sd) + f"{md+1:02}" + "_mean_pulse.jpeg")
        plt.savefig(plots_path   + "/mean_pulse/"  + sides_map.get(sd) + f"{md+1:02}" + "_mean_pulse.jpeg")
        plt.close()

for sd in sides_map:
    for md in mods_map:
        plt.figure(figsize = (20, 12))
        for ch in cells_map:
            plt.subplot(2,2,ch+1)
            plt.plot(pulses_axis, norm_pulse[sd,md,ch,:])
            plt.title("Normalized mean pulse | " + sides_map.get(sd) + f"{md+1:02}" + " - " + channel.get(ch))
            plt.xlabel("Sample")
            plt.ylabel("Amplitude [ADC]")
            plt.grid()
        output_path = plots_path + "/all_modules/"     + sides_map.get(sd) + f"{md+1:02}"
        plt.savefig(output_path  + "/"                 + sides_map.get(sd) + f"{md+1:02}" + "_mean_pulse_norm.jpeg")
        plt.savefig(plots_path   + "/mean_pulse_norm/" + sides_map.get(sd) + f"{md+1:02}" + "_mean_pulse_norm.jpeg")
        plt.close()

print(">> Plot pedestal, samples and mean pulses... Done!\n")

print(">> Calculate and plot the covariance matrix...")

for sd in sides_map:
    for md in mods_map:
        desc_str = "Processing " + sides_map.get(sd) + f"{md+1:02}"
        for ch in tqdm(cells_map, desc=desc_str):
            C[sd, md, ch,:,:] = robust_cov(sampleZB[:, sd, md, ch, :].T)

for sd in sides_map:
    for md in mods_map:
        plt.figure(figsize = (20, 12))
        for ch in cells_map:
            plt.subplot(2,2,ch+1)
            sns.heatmap(C[sd, md, ch,:,:], annot=True, fmt='g')
            plt.title("Robust covariance matrix | " + sides_map.get(sd) + f"{md+1:02}" + " - " + channel.get(ch))
        output_path = plots_path + "/all_modules/"  + sides_map.get(sd) + f"{md+1:02}"
        plt.savefig(output_path  + "/"              + sides_map.get(sd) + f"{md+1:02}" + "_covariance.jpeg")
        plt.savefig(plots_path   + "/covariance/"   + sides_map.get(sd) + f"{md+1:02}" + "_covariance.jpeg")
        plt.close()

print(">> Calculate and plot the covariance matrix... Done!\n")

print(">> Calculate and plot the inverse covariance matrix...")

for sd in sides_map:
    for md in mods_map:
        for ch in cells_map:
            C_inv[sd, md, ch,:,:] = np.linalg.inv(C[sd, md, ch,:,:])

for sd in sides_map:
    for md in mods_map:
        plt.figure(figsize = (20, 12))
        for ch in cells_map:
            plt.subplot(2,2,ch+1)
            sns.heatmap(C_inv[sd, md, ch,:,:], annot=True, fmt='g')
            plt.title("Inverse covariance matrix | " + sides_map.get(sd) + f"{md+1:02}" + " - " + channel.get(ch))
        output_path = plots_path + "/all_modules/"   + sides_map.get(sd) + f"{md+1:02}"
        plt.savefig(output_path + "/"                + sides_map.get(sd) + f"{md+1:02}" + "_covariance_inv.jpeg")
        plt.savefig(plots_path  + "/covariance_inv/" + sides_map.get(sd) + f"{md+1:02}" + "_covariance_inv.jpeg")
        plt.close()

print(">> Calculate and plot the inverse covariance matrix... Done!\n")

print(">> Calculate and plot the filter weights...")

for sd in sides_map:
    for md in mods_map:
        for ch in cells_map:
            h   = norm_pulse[sd,md,ch,:]
            num = np.dot(h, C_inv[sd, md, ch,:,:])
            den = (np.dot(num, h.T))
            w[sd,md,ch,:] = num/den

for sd in sides_map:
    for md in mods_map:
        plt.figure(figsize = (20, 12))
        for ch in cells_map:
            plt.subplot(2,2,ch+1)
            plt.plot(pulses_axis, w[sd,md,ch,:])
            plt.title("Weights | " + sides_map.get(sd) + f"{md+1:02}" + " - " + channel.get(ch))
            plt.xlabel("Sample")
            plt.ylabel("Amplitude")
            plt.grid()
        output_path = plots_path + "/all_modules/" + sides_map.get(sd) + f"{md+1:02}"
        plt.savefig(output_path  + "/"             + sides_map.get(sd) + f"{md+1:02}" + "_weights.jpeg")
        plt.savefig(plots_path   + "/weights/"     + sides_map.get(sd) + f"{md+1:02}" + "_weights.jpeg")
        plt.close()

print(">> Calculate and plot the filter weights... Done!\n")

print(">> Calculate and plot the fitting...")

for sd in sides_map:
    for md in mods_map:
        p = [[], [] , [], []]
        for evt in events_map:
            for ch in cells_map:
                p[ch].append(samples_ped[evt,sd,md,ch,:])

for sd in sides_map:
    for md in mods_map:
        x = [[], [] , [], []]
        y = [[], [] , [], []]
        plt.figure(figsize = (20, 12))
        for ch in cells_map:
            for i in range(0, np.size(p[ch], axis=0)):
                x[ch].append(p[ch][i][2])
                y[ch].append(np.dot(w[sd,md,ch,:],np.array(p[ch][i][:]).T))
            plt.subplot(2,2,ch+1)
            plt.plot(x[ch], y[ch], 'x')
            plt.title("Fit | " + sides_map.get(sd) + f"{md+1:02}" + " - " + channel.get(ch))
            plt.xlabel("p")
            plt.ylabel("w*p")
            plt.grid()
        output_path = plots_path + "/all_modules/" + sides_map.get(sd) + f"{md+1:02}"
        plt.savefig(output_path  + "/"             + sides_map.get(sd) + f"{md+1:02}" + "_filter.jpeg")
        plt.savefig(plots_path   + "/filter/"      + sides_map.get(sd) + f"{md+1:02}" + "_filter.jpeg")
        plt.close()

for sd in sides_map:
    for md in mods_map:
        for ch in cells_map:
            for i in range(0, pulses):
                quant_w[sd,md,ch,i] = (w[sd,md,ch,i]/np.max(w[sd,md,ch,:]))*511

quant_w   = quant_w.astype("int")

for sd in sides_map:
    for md in mods_map:
        plt.figure(figsize = (20, 12))
        xq        = [[], [] , [], []]
        yq        = [[], [] , [], []]
        coef      = [[], [] , [], []]
        poly1d_fn = [[], [] , [], []]
        for ch in cells_map:
            for evt in range(0, np.size(sampleMuon, 0)):
                xq[ch].append(np.dot(quant_w[sd,md,ch,:], sampleMuon[evt,sd,md,ch,:]))
                yq[ch].append(eOptMuon[evt,sd,md,ch,0])
        for ch in cells_map:
            coef[ch]       = np.polyfit(xq[ch],yq[ch],1)
            poly1d_fn[ch]  = np.poly1d(coef[ch])
            e500[sd,md,ch] = (threshold - coef[ch][1])/coef[ch][0]

            plt.subplot(2,2,ch+1)
            plt.plot(xq[ch], yq[ch], '*', xq[ch], poly1d_fn[ch](xq[ch]))
            plt.plot(e500[sd,md,ch], threshold, "mD")
            plt.title("Fit | " + sides_map.get(sd) + f"{md+1:02}" + " - " + channel.get(ch))
            plt.ylabel('Energy [MeV]')
            plt.xlabel('W * Quantized Sample')
            plt.grid()
        output_path = plots_path + "/all_modules/" + sides_map.get(sd) + f"{md+1:02}"
        plt.savefig(output_path  + "/"             + sides_map.get(sd) + f"{md+1:02}" +  "_fit.png")
        plt.savefig(plots_path   + "/fit/"         + sides_map.get(sd) + f"{md+1:02}" + "_fit.jpeg")
        plt.close()

print(">> Calculate and plot the fitting... Done!\n")

print(">> Calculate relative std for D5, D6 and D5+D6...")

# Relative std for D5L cell

n=0
m=0

for sd in sides_map:
    for md in mods_map:
        zb  = []
        wzb = []
        for i in range(0, entries):
            zb.append(sampleZB[i, sd, md, m, 2])
            aux_dot = np.dot(w[sd, md, m], (sampleZB[i, sd, md, m, :].T))
            wzb.append(aux_dot)
        old_std[sd,md,n]   = np.std(zb)
        new_std[sd,md,n]   = np.std(wzb)
        std_relat[sd,md,n] = (new_std[sd,md,n]-old_std[sd,md,n])/old_std[sd,md,n]


# Relative std for D5R cell

n=1
m=1

for sd in sides_map:
    for md in mods_map:
        zb  = []
        wzb = []
        for i in range(0, entries):
            zb.append(sampleZB[i, sd, md, m, 2])
            aux_dot = np.dot(w[sd, md, m], (sampleZB[i, sd, md, m, :].T))
            wzb.append(aux_dot)
        old_std[sd,md,n]   = np.std(zb)
        new_std[sd,md,n]   = np.std(wzb)
        std_relat[sd,md,n] = (new_std[sd,md,n]-old_std[sd,md,n])/old_std[sd,md,n]

# Relative std for D6L cell

n=2
m=2

for sd in sides_map:
    for md in mods_map:
        zb  = []
        wzb = []
        for i in range(0, entries):
            zb.append(sampleZB[i, sd, md, m, 2])
            aux_dot = np.dot(w[sd, md, m], (sampleZB[i, sd, md, m, :].T))
            wzb.append(aux_dot)
        old_std[sd,md,n]   = np.std(zb)
        new_std[sd,md,n]   = np.std(wzb)
        std_relat[sd,md,n] = (new_std[sd,md,n]-old_std[sd,md,n])/old_std[sd,md,n]


# Relative std for D6R cell

n=3
m=3

for sd in sides_map:
    for md in mods_map:
        zb  = []
        wzb = []
        for i in range(0, entries):
            zb.append(sampleZB[i, sd, md, m, 2])
            aux_dot = np.dot(w[sd, md, m], (sampleZB[i, sd, md, m, :].T))
            wzb.append(aux_dot)
        old_std[sd,md,n]   = np.std(zb)
        new_std[sd,md,n]   = np.std(wzb)
        std_relat[sd,md,n] = (new_std[sd,md,n]-old_std[sd,md,n])/old_std[sd,md,n]

# Relative std for D5 cell

n=4

for sd in sides_map:
    for md in mods_map:
        zb  = []
        wzb = []
        for i in range(0, entries):
            zb.append(sampleZB[i, sd, md, 0, 2] + sampleZB[i, sd, md, 1, 2])
            aux_dot = np.dot(w[sd, md, 0], (sampleZB[i, sd, md, 0, :].T)) + np.dot(w[sd, md, 1], (sampleZB[i, sd, md, 1, :].T))
            wzb.append(aux_dot)
        old_std[sd,md,n]   = np.std(zb)
        new_std[sd,md,n]   = np.std(wzb)
        std_relat[sd,md,n] = (new_std[sd,md,n]-old_std[sd,md,n])/old_std[sd,md,n]

# Relative std for D6 cell

n=5

for sd in sides_map:
    for md in mods_map:
        zb  = []
        wzb = []
        for i in range(0, entries):
            zb.append(sampleZB[i, sd, md, 2, 2] + sampleZB[i, sd, md, 3, 2])
            aux_dot = np.dot(w[sd, md, 2], (sampleZB[i, sd, md, 2, :].T)) + np.dot(w[sd, md, 3], (sampleZB[i, sd, md, 3, :].T))
            wzb.append(aux_dot)
        old_std[sd,md,n]   = np.std(zb)
        new_std[sd,md,n]   = np.std(wzb)
        std_relat[sd,md,n] = (new_std[sd,md,n]-old_std[sd,md,n])/old_std[sd,md,n]

# Relative std for D5 + D6 cells

n=6

for sd in sides_map:
    for md in mods_map:
        zb  = []
        wzb = []
        for i in range(0, entries):
            zb.append(sampleZB[i, sd, md, 0, 2] + sampleZB[i, sd, md, 1, 2] + sampleZB[i, sd, md, 2, 2] + sampleZB[i, sd, md, 3, 2])
            aux_dot = np.dot(w[sd, md, 0], (sampleZB[i, sd, md, 0, :].T)) + np.dot(w[sd, md, 1], (sampleZB[i, sd, md, 1, :].T)) + np.dot(w[sd, md, 2], (sampleZB[i, sd, md, 2, :].T)) + np.dot(w[sd, md, 3], (sampleZB[i, sd, md, 3, :].T))
            wzb.append(aux_dot)
        old_std[sd,md,n]   = np.std(zb)
        new_std[sd,md,n]   = np.std(wzb)
        std_relat[sd,md,n] = (new_std[sd,md,n]-old_std[sd,md,n])/old_std[sd,md,n]

print(">> Calculate relative std for D5, D6 and D5+D6... Done!\n")

print(">> Save all parameters for each cell...")

np.save('../../data/data_' + run_number + '/'+ run_number + '_' + 'mean_pulse.npy',   mean_pulse)
np.save('../../data/data_' + run_number + '/'+ run_number + '_' + 'norm_pulse.npy',   norm_pulse)
np.save('../../data/data_' + run_number + '/'+ run_number + '_' + 'pedestal.npy',       pedestal)
np.save('../../data/data_' + run_number + '/'+ run_number + '_' + 'samples_ped.npy', samples_ped)
np.save('../../data/data_' + run_number + '/'+ run_number + '_' + 'C.npy',                     C)
np.save('../../data/data_' + run_number + '/'+ run_number + '_' + 'C_inv.npy',             C_inv)
np.save('../../data/data_' + run_number + '/'+ run_number + '_' + 'w.npy',                     w)
np.save('../../data/data_' + run_number + '/'+ run_number + '_' + 'quant_w.npy',         quant_w)
np.save('../../data/data_' + run_number + '/'+ run_number + '_' + 'std_relat.npy',     std_relat)

print(">> Save all parameters for each cell... Done!\n")

print(" ------------------- END -------------------")
