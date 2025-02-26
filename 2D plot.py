import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ---- STEP 1: Load Raman Data ----
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

# First Plot: 1200-1700 cm⁻¹ (Raman Waterfall Plot)
ax1 = fig.add_subplot(121, projection='3d')
X_1200_1700, Y_1200_1700 = np.meshgrid(unique_shifts_1200_1700, unique_times)
Z_1200_1700 = intensity_matrix_1200_1700

# Plot surface
ax1.plot_surface(X_1200_1700, Y_1200_1700, Z_1200_1700, cmap="plasma")

ax1.set_xlabel("Raman Shift (cm⁻¹)")
ax1.set_ylabel("Time (hours)")
ax1.set_zlabel("Normalized Intensity")
ax1.set_title("D and G band evolution during 1st Discharge")

# ---- STEP 7: Create 2D Potential vs Time Plot on (110) Plane ----
ax2 = fig.add_subplot(122, projection='3d')

# Load potential data
potential_file_path = r"C:\Users\StdUser\PycharmProjects\PythonProject\potential_data_LHCE3.txt"
potential_data = np.loadtxt(potential_file_path, skiprows=1)

# Extract potential data
time_potential = potential_data[:, 0]  # Already in hours
potential = potential_data[:, 1]

# Apply the same time filter for potential data
potential_time_filtered = time_potential[(time_potential >= 0) & (time_potential <= 18)]
potential_filtered = potential[(time_potential >= 0) & (time_potential <= 18)]

# Prepare data for plotting on the (110) plane (Z=0)
time_for_plot = potential_time_filtered
potential_for_plot = potential_filtered
Z_for_plot = np.zeros_like(potential_for_plot)  # Z values set to 0 to ground the plot

# **Swapped Axes: Time on Y, Potential on X**
ax2.plot(potential_for_plot, time_for_plot, Z_for_plot, color='green')

# Set labels (Swapped)
ax2.set_xlabel('Potential (V)')   # Now X-axis
ax2.set_ylabel('Time (hours)')    # Now Y-axis
ax2.set_zlabel('Z (arbitrary)')
ax2.set_title('Potential vs Time on (110) plane')

# Set the Z-axis limits (0 to 0.001)
ax2.set_zlim(0, 0.001)

# **Ensure Axes are Properly Flipped**
ax2.invert_xaxis()  # Invert potential axis (flipped scale)
#ax2.invert_yaxis()  # Invert time axis

# **Hide the Z-axis to make the plot appear on the plane**
ax2.zaxis.line.set_lw(0)  # Hide the Z-axis line
ax2.set_zticks([])  # Remove Z-axis ticks
ax2.grid(False)  # Hide the grid

# ---- STEP 8: Display the Combined Plot ----
plt.tight_layout()  # Adjust layout for better spacing
plt.savefig("combined_plot_with_potential_swapped_axes.png", format="png")  # Save the plot
plt.show()
