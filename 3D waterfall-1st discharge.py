import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ---- STEP 1: Load Data ----
file_path = r"C:\Users\StdUser\PycharmProjects\PythonProject\LHCE3-baselined.txt"
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

# ---- STEP 3: Process Data for 1200-1700 cm⁻¹ ----
mask_1200_1700 = (raman_shift_filtered >= 1200) & (raman_shift_filtered <= 1700)
data_1200_1700 = filtered_data[mask_1200_1700]

time_1200_1700 = data_1200_1700[:, 0] / 3600
raman_shift_1200_1700 = data_1200_1700[:, 1]
intensity_1200_1700 = data_1200_1700[:, 2]

# ---- STEP 4: Normalize Intensity ----
# Normalize intensity by dividing by the max intensity value
intensity_max = np.max(intensity_1200_1700)
intensity_1200_1700_normalized = intensity_1200_1700 / intensity_max

# ---- STEP 5: Create 2D Grid for Intensity Matrix ----
unique_times = np.unique(time_filtered)
unique_shifts_1200_1700 = np.unique(raman_shift_1200_1700)

intensity_matrix_1200_1700 = np.zeros((len(unique_times), len(unique_shifts_1200_1700)))

# Fill intensity matrix for 1200-1700 cm⁻¹
for i, t in enumerate(unique_times):
    for j, shift in enumerate(unique_shifts_1200_1700):
        mask = (time_1200_1700 == t) & (raman_shift_1200_1700 == shift)
        if np.any(mask):
            intensity_matrix_1200_1700[i, j] = intensity_1200_1700_normalized[mask][0]

# ---- STEP 6: Create 3D Waterfall Plot ----
fig = plt.figure(figsize=(12, 8))

# First Plot: 1200-1700 cm⁻¹
ax1 = fig.add_subplot(111, projection='3d')
X_1200_1700, Y_1200_1700 = np.meshgrid(unique_shifts_1200_1700, unique_times)
Z_1200_1700 = intensity_matrix_1200_1700

# Plot surface
ax1.plot_surface(X_1200_1700, Y_1200_1700, Z_1200_1700, cmap="plasma")

ax1.set_xlabel("Raman Shift (cm⁻¹)")
ax1.set_ylabel("Time (hours)")
ax1.set_zlabel("Normalized Intensity")
ax1.set_title("D and G band evolution during 1st Discharge")

# Adjust layout for better spacing
plt.tight_layout()
# Save the plot as PNG
plt.savefig("waterfall_plot_1200_1700_normalized.png", format="png")
# Show the final figure
plt.show()
