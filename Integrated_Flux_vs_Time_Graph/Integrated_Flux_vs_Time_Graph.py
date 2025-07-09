#Integrated Flux vs Time

import cdflib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import timedelta

#List your 3 consecutive TH2 CDF file paths here
cdf_paths = [
    r"CDF_file_path_day1.cdf",
    r"CDF_file_path_day2.cdf",
    r"CDF_file_path_day3.cdf"
]

#Containers to collect data from all files
all_times = []
all_fluxes = []

#Loop through each file and extract data
for path in cdf_paths:
    try:
        cdf_file = cdflib.CDF(path)
        time_data = cdf_file.varget('epoch_for_cdf_mod')
        flux_data = cdf_file.varget('integrated_flux_mod')
        time_dt = cdflib.cdfepoch.to_datetime(time_data)
        integrated_flux = np.nansum(flux_data, axis=1)  # sum across energy
        all_times.extend(time_dt)
        all_fluxes.extend(integrated_flux)
    except Exception as e:
        print(f"⚠ Could not read {path}: {e}")

#Convert to NumPy arrays
all_times = pd.to_datetime(np.array(all_times))
all_fluxes = np.array(all_fluxes)

#Label for the plot title
start_day = all_times.min().strftime('%Y-%m-%d')
end_day = (all_times.max()).strftime('%Y-%m-%d')

#Plot
plt.figure(figsize=(14, 6))
plt.plot(all_times, all_fluxes, color='darkblue', linewidth=1.3)

plt.suptitle("SWIS TH2 – Integrated Ion Flux vs Time", fontsize=16, y=0.96)
plt.title(f"Observation Period: {start_day} to {end_day}", fontsize=12)

plt.xlabel("Time (UTC)", fontsize=12)
plt.ylabel("Integrated Flux [particles/cm²/s/sr]", fontsize=12)
plt.grid(True)

#Fixed Y-axis for consistent comparison
plt.ylim(0, 3e9)

#Format x-axis
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
plt.gcf().autofmt_xdate()
plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.show()