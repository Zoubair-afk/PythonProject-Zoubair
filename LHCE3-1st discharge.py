import numpy as np
import matplotlib.pyplot as plt

# ---- STEP 1: Load Data ----
file_path = r"C:\Users\StdUser\PycharmProjects\PythonProject\LHCE3.txt"
data = np.loadtxt(file_path, skiprows=1)

# Extract columns
time = data[:, 0] / 3600  # Convert seconds to hours
raman_shift = data[:, 1]
intensity = data[:, 2]

# ---- STEP 2: Apply Time Filter (0 to 18 Hours) ----
time_mask = (time >= 0) & (time <= 18)
filtered_data = data[time_mask]

time_filtered = filtered_data[:, 0] / 3600
raman_shift_filtered = filtered_data[:, 1]
intensity_filtered = filtered_data[:, 2]

# ---- STEP 3: Process Data for Two Ranges ----
# (A) For 1000-1750 cm⁻¹
mask_1000_1750 = (raman_shift_filtered >= 1000) & (raman_shift_filtered <= 1750)
data_1000_1750 = filtered_data[mask_1000_1750]

time_1000_1750 = data_1000_1750[:, 0] / 3600
raman_shift_1000_1750 = data_1000_1750[:, 1]
intensity_1000_1750 = data_1000_1750[:, 2]

# (B) For 150-300 cm⁻¹
mask_150_300 = (raman_shift_filtered >= 150) & (raman_shift_filtered <= 300)
data_150_300 = filtered_data[mask_150_300]

time_150_300 = data_150_300[:, 0] / 3600
raman_shift_150_300 = data_150_300[:, 1]
intensity_150_300 = data_150_300[:, 2]

# ---- STEP 4: Create 2D Grids ----
unique_times = np.unique(time_filtered)
unique_shifts_1000_1750 = np.unique(raman_shift_1000_1750)
unique_shifts_150_300 = np.unique(raman_shift_150_300)

# Create intensity matrices
intensity_matrix_1000_1750 = np.zeros((len(unique_times), len(unique_shifts_1000_1750)))
intensity_matrix_150_300 = np.zeros((len(unique_times), len(unique_shifts_150_300)))

# Fill intensity matrices
for i, t in enumerate(unique_times):
    for j, shift in enumerate(unique_shifts_1000_1750):
        mask = (time_1000_1750 == t) & (raman_shift_1000_1750 == shift)
        if np.any(mask):
            intensity_matrix_1000_1750[i, j] = intensity_1000_1750[mask][0]

    for j, shift in enumerate(unique_shifts_150_300):
        mask = (time_150_300 == t) & (raman_shift_150_300 == shift)
        if np.any(mask):
            intensity_matrix_150_300[i, j] = intensity_150_300[mask][0]

# ---- STEP 5: Create Side-by-Side Contour Plots ----
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# First Plot: 1000-1750 cm⁻¹
ax1 = axes[0]
contour1 = ax1.contourf(unique_shifts_1000_1750, unique_times, intensity_matrix_1000_1750, levels=100, cmap="plasma")
ax1.set_ylim([0, 18])  # Limit time to 0-18 hours
ax1.invert_yaxis()
cbar1 = fig.colorbar(contour1, ax=ax1)
cbar1.set_label("Intensity (a.u.)")
ax1.set_xlabel("Raman Shift (cm⁻¹)")
ax1.set_ylabel("Time (hours)")
ax1.set_title("Operando Raman Contour Map (1000-1750 cm⁻¹)")

# Second Plot: 150-300 cm⁻¹
ax2 = axes[1]
contour2 = ax2.contourf(unique_shifts_150_300, unique_times, intensity_matrix_150_300, levels=100, cmap="plasma")
ax2.set_ylim([0, 18])  # Limit time to 0-18 hours
ax2.invert_yaxis()
cbar2 = fig.colorbar(contour2, ax=ax2)
cbar2.set_label("Intensity (a.u.)")
ax2.set_xlabel("Raman Shift (cm⁻¹)")
ax2.set_ylabel("Time (hours)")
ax2.set_title("Operando Raman Contour Map (150-300 cm⁻¹)")

# Adjust layout for better spacing
plt.tight_layout(pad=4.0)

# Show the final figure
plt.show()
