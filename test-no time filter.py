import numpy as np
import matplotlib.pyplot as plt

# ---- STEP 1: Load Data ----
file_path = r"C:\Users\StdUser\PycharmProjects\PythonProject\ECEDEC-10-10s-spotparticle-cell5-1sep_Copy.txt"
data = np.loadtxt(file_path, skiprows=1)

# Extract columns
time = data[:, 0]         # Time (seconds)
raman_shift = data[:, 1]  # Raman Shift (cm⁻¹)
intensity = data[:, 2]    # Intensity (a.u.)

# Convert time to hours
time_in_hours = time / 3600

# ---- STEP 2: Process Data for Two Ranges ----
# (A) For 1000-1750 cm⁻¹
mask_1000_1750 = (raman_shift >= 1000) & (raman_shift <= 1750)
data_1000_1750 = data[mask_1000_1750]

time_1000_1750 = data_1000_1750[:, 0] / 3600
raman_shift_1000_1750 = data_1000_1750[:, 1]
intensity_1000_1750 = data_1000_1750[:, 2]

# (B) For 150-300 cm⁻¹
mask_150_300 = (raman_shift >= 150) & (raman_shift <= 300)
data_150_300 = data[mask_150_300]

time_150_300 = data_150_300[:, 0] / 3600
raman_shift_150_300 = data_150_300[:, 1]
intensity_150_300 = data_150_300[:, 2]

# ---- STEP 3: Create 2D Grids ----
unique_times = np.unique(time_in_hours)
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

# ---- STEP 4: Create Side-by-Side Contour Plots ----
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# First Plot: 1000-1750 cm⁻¹
ax1 = axes[0]
contour1 = ax1.contourf(unique_shifts_1000_1750, unique_times, intensity_matrix_1000_1750, levels=100, cmap="plasma")
ax1.set_ylim([0, max(unique_times)])
ax1.invert_yaxis()
cbar1 = fig.colorbar(contour1, ax=ax1)
cbar1.set_label("Intensity (a.u.)")
ax1.set_xlabel("Raman Shift (cm⁻¹)")
ax1.set_ylabel("Time (hours)")
ax1.set_title("Operando Raman Contour Map (1000-1750 cm⁻¹)")

# Second Plot: 150-300 cm⁻¹
ax2 = axes[1]
contour2 = ax2.contourf(unique_shifts_150_300, unique_times, intensity_matrix_150_300, levels=100, cmap="plasma")
ax2.set_ylim([0, max(unique_times)])
ax2.invert_yaxis()
cbar2 = fig.colorbar(contour2, ax=ax2)
cbar2.set_label("Intensity (a.u.)")
ax2.set_xlabel("Raman Shift (cm⁻¹)")
ax2.set_ylabel("Time (hours)")
ax2.set_title("Operando Raman Contour Map (150-300 cm⁻¹)")

# ---- STEP 5: Add Dashed Lines for Charge/Discharge ----
charge_times = [0.09, 10.78]
discharge_times = [5.45]

for ax in [ax1, ax2]:  # Apply to both plots
    for time_point in charge_times:
        ax.axhline(y=time_point, color='red', linestyle='--', linewidth=1)  # Red dashed line for charge
    for time_point in discharge_times:
        ax.axhline(y=time_point, color='blue', linestyle='--', linewidth=1)  # Blue dashed line for discharge

# ---- STEP 6: Add Charge/Discharge Labels ----
for ax in [ax1, ax2]:  # Apply to both plots
    for i in range(len(charge_times)):
        charge_time = charge_times[i]
        discharge_time = discharge_times[i] if i < len(discharge_times) else None

        if discharge_time and charge_time < discharge_time:
            midpoint = (charge_time + discharge_time) / 2
            ax.text(
                x=(ax.get_xlim()[0] + ax.get_xlim()[1]) / 2, y=midpoint,
                s="Charge", color='red', ha='center', va='center', fontsize=12, weight='bold'
            )

        if discharge_time and charge_time < discharge_time:
            midpoint = (charge_time + discharge_time) / 2
            ax.text(
                x=(ax.get_xlim()[0] + ax.get_xlim()[1]) / 2, y=midpoint,
                s="Discharge", color='blue', ha='center', va='center', fontsize=12, weight='bold'
            )

# Adjust layout for better spacing
plt.tight_layout(pad=4.0)

# Show the final figure
plt.show()
