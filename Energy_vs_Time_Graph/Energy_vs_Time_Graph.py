#Energy vs Time

import cdflib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

#Just change this line to the .cdf file you want to analyze
cdf_path = r"CDF_file_path.cdf"

#Extract date from the filename
filename = os.path.basename(cdf_path)
date_part = filename.split('_')[4][:8]  # '20250522'
date_str = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:]}"  # '2025-05-22'

#Load the CDF file
cdf_file = cdflib.CDF(cdf_path)

#Extract variables
time_raw = cdf_file.varget('epoch_for_cdf_mod')
energy_bins_raw = cdf_file.varget('energy_center_mod')
flux_data = cdf_file.varget('integrated_flux_mod')

#Convert time to datetime
time_converted = cdflib.cdfepoch.to_datetime(time_raw)

#Fix energy_bins shape: use first time slice
energy_bins = np.array(energy_bins_raw[0])  # 1D array

#Convert to log scale
flux_log = np.log10(np.array(flux_data) + 1e-10)

#Ensure shape (energy_bins, time_points)
if flux_log.shape[0] == len(time_converted):
    flux_log = flux_log.T  # Transpose to (energy_bins, time)

#Plot
plt.figure(figsize=(12, 6))
plt.imshow(flux_log, aspect='auto', origin='lower', cmap='inferno',
           extent=[mdates.date2num(time_converted[0]), mdates.date2num(time_converted[-1]),
                   energy_bins[0], energy_bins[-1]])

#Format time axis
plt.gca().xaxis_date()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(rotation=45)

#Labels and title
plt.xlabel("Time (UTC)")
plt.ylabel("Energy (keV)")
plt.title(f"Log-scaled Flux Spectrogram from TH2\nDate: {date_str}")

#Colorbar
cbar = plt.colorbar(label='log₁₀(Flux)')
cbar.ax.set_ylabel('log₁₀(Flux)', rotation=270, labelpad=15)

plt.tight_layout()
plt.show()