# Density, Temperature, Velocity vs Time

import cdflib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# List of CDF files to read data from (replace with actual file paths)
cdf_paths = [
    r"CDF_file_path_day1.cdf",
    r"CDF_file_path_day2.cdf",
    r"CDF_file_path_day3.cdf"
]

# Lists to store data from all files
all_times, all_density, all_temperature, all_velocity = [], [], [], []

# Loop through each CDF file and extract required variables
for path in cdf_paths:
    try:
        cdf = cdflib.CDF(path)

        # Read time variable and convert to datetime
        time_data = cdf.varget('epoch_for_cdf_mod')
        time_dt = cdflib.cdfepoch.to_datetime(time_data)

        # Read plasma parameters
        density = cdf.varget('proton_density')
        temperature = cdf.varget('proton_thermal')
        velocity = cdf.varget('proton_bulk_speed')

        # Append data to lists
        all_times.extend(time_dt)
        all_density.extend(density)
        all_temperature.extend(temperature)
        all_velocity.extend(velocity)

    except Exception as e:
        # Print warning if file cannot be read
        print(f"⚠ Could not read {path}: {e}")

# Convert lists to numpy arrays and pandas datetime for easier handling
all_times = pd.to_datetime(np.array(all_times))
all_density = np.array(all_density)
all_temperature = np.array(all_temperature)
all_velocity = np.array(all_velocity)

# Replace fill values (e.g., 1e+31) with NaN for proper plotting
def clean_array(arr, fill_threshold=1e30):
    arr = np.array(arr, dtype=np.float64)
    arr[(arr > fill_threshold) | (arr < -fill_threshold)] = np.nan
    return arr

all_density = clean_array(all_density)
all_temperature = clean_array(all_temperature)
all_velocity = clean_array(all_velocity)

# Remove NaN values to avoid breaks in the plot lines
def filter_valid_data(times, values):
    mask = ~np.isnan(values)
    return times[mask], values[mask]

time_density, val_density = filter_valid_data(all_times, all_density)
time_temp, val_temp = filter_valid_data(all_times, all_temperature)
time_vel, val_vel = filter_valid_data(all_times, all_velocity)

# Create a 3-row subplot for density, temperature, and velocity
fig, axs = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

# Plot proton number density vs time
axs[0].plot(time_density, val_density, color='green', linewidth=1.5)
axs[0].set_ylabel("Density (cm⁻³)")
axs[0].set_title("Proton Number Density")
axs[0].grid(True)

# Plot proton thermal temperature vs time
axs[1].plot(time_temp, val_temp, color='red', linewidth=1.5)
axs[1].set_ylabel("Temperature (eV)")
axs[1].set_title("Proton Thermal Temperature")
axs[1].grid(True)

# Plot proton bulk velocity vs time
axs[2].plot(time_vel, val_vel, color='blue', linewidth=1.5)
axs[2].set_ylabel("Velocity (km/s)")
axs[2].set_title("Proton Bulk Velocity")
axs[2].grid(True)

# Set x-axis date format for better readability
axs[2].xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))

plt.xlabel("Time (UTC)", fontsize=12)
fig.suptitle("SWIS BLK – Plasma Parameters vs Time", fontsize=16)
fig.subplots_adjust(top=0.93)
plt.gcf().autofmt_xdate(rotation=45)  # rotate for spacing
plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.show()