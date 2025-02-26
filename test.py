import numpy as np
import matplotlib.pyplot as plt

# ---- STEP 1: Load Data ----
file_path = r"C:\Users\StdUser\PycharmProjects\PythonProject\LHCE3.txt"
data = np.loadtxt(file_path, skiprows=1)

# Extract columns
time = data[:, 0]         # First column → Time (in seconds)
raman_shift = data[:, 1]  # Second column → Raman Shift (Y-axis)
intensity = data[:, 2]    # Third column → Intensity (Z-axis)

# ---- STEP 2: Convert Time to Hours ----
time_in_hours = time / 3600  # Convert time from seconds to hours

# ---- STEP 3: Filter Data for Raman Shift Between 1000 and 1750 cm⁻¹ ----
mask = (raman_shift >= 1000) & (raman_shift <= 1750)
filtered_data = data[mask]

# Extract filtered columns
time_filtered = filtered_data[:, 0] / 3600  # Convert filtered time to hours
raman_shift_filtered = filtered_data[:, 1]
intensity_filtered = filtered_data[:, 2]

# ---- STEP 4: Reshape Data into 2D Grid (for filtered data) ----
unique_times = np.unique(time_filtered)
unique_shifts = np.unique(raman_shift_filtered)

# Create a 2D intensity matrix (rows = time, columns = Raman shift)
intensity_matrix = np.zeros((len(unique_times), len(unique_shifts)))

# Fill the matrix by matching (time, Raman Shift) pairs
for i, t in enumerate(unique_times):
    for j, shift in enumerate(unique_shifts):
        mask = (time_filtered == t) & (raman_shift_filtered == shift)
        if np.any(mask):
            intensity_matrix[i, j] = intensity_filtered[mask][0]

# ---- STEP 5: Create Contour Plot ----
plt.figure(figsize=(8, 6))

# Generate contour plot
contour = plt.contourf(unique_shifts, unique_times, intensity_matrix, levels=100, cmap="plasma")

# Fixing Y-axis scaling for time to start from 18 hours
plt.ylim(min(unique_times), max(unique_times))  # Ensure time is displayed in the right range
plt.gca().invert_yaxis()  # Invert Y-axis if time increases from bottom to top

# Set the Y-axis limits to start from hour 18 (even if data doesn't start there)
plt.ylim([18, max(unique_times)])

# Color bar and labels
cbar = plt.colorbar(contour)
cbar.set_label("Intensity (a.u.)")
plt.xlabel("Raman Shift (cm⁻¹)")
plt.ylabel("Time (hours)")  # Update label to 'Time (hours)'
plt.title("Operando Raman Contour Map (1000-1750 cm⁻¹)")
# ---- STEP 6: Add Alternating Dashed Lines ----
# Define times where you want to add dashed lines (e.g., 18.5h, 19h, etc.)
charge_times = [19, 36.84, 55.64, 74.77 ]  # Example charge times
discharge_times = [27.04, 45.82, 64.9, 83.97]  # Example discharge times

# Add dashed lines for charge (red)
for time_point in charge_times:
    plt.axhline(y=time_point, color='red', linestyle='--', linewidth=1)  # Red dashed line for charge

# Add dashed lines for discharge (blue)
for time_point in discharge_times:
    plt.axhline(y=time_point, color='blue', linestyle='--', linewidth=1)  # Blue dashed line for discharge
# ---- STEP 7: Add Labels Between Lines ----
# Loop over both charge and discharge times
for i in range(min(len(charge_times), len(discharge_times))):
    charge_time = charge_times[i]
    discharge_time = discharge_times[i]

    # Ensure that we place 'Charge' label between the charge and discharge lines
    if charge_time < discharge_time:
        midpoint = (charge_time + discharge_time) / 2
        plt.text(
            x=unique_shifts[len(unique_shifts) // 2], y=midpoint,
            s="Charge", color='red', ha='center', va='center', fontsize=12, weight='bold'
        )
        # Also ensure we place 'Discharge' label on the opposite side
        midpoint_next = (discharge_time + charge_times[i + 1]) / 2 if i + 1 < len(charge_times) else discharge_time
        plt.text(
            x=unique_shifts[len(unique_shifts) // 2], y=midpoint_next,
            s="Discharge", color='blue', ha='center', va='center', fontsize=12, weight='bold'
        )

# ---- STEP 1: Filter Data for Raman Shift Between 150 and 300 cm⁻¹ ----
mask_150_300 = (raman_shift >= 150) & (raman_shift <= 300)
filtered_data_150_300 = data[mask_150_300]

# Extract filtered columns for the second plot
time_filtered_150_300 = filtered_data_150_300[:, 0] / 3600  # Convert filtered time to hours
raman_shift_filtered_150_300 = filtered_data_150_300[:, 1]
intensity_filtered_150_300 = filtered_data_150_300[:, 2]

# ---- STEP 2: Reshape Data into 2D Grid (for second plot) ----
unique_times_150_300 = np.unique(time_filtered_150_300)
unique_shifts_150_300 = np.unique(raman_shift_filtered_150_300)

# Create a 2D intensity matrix (rows = time, columns = Raman shift)
intensity_matrix_150_300 = np.zeros((len(unique_times_150_300), len(unique_shifts_150_300)))

# Fill the matrix by matching (time, Raman Shift) pairs
for i, t in enumerate(unique_times_150_300):
    for j, shift in enumerate(unique_shifts_150_300):
        mask = (time_filtered_150_300 == t) & (raman_shift_filtered_150_300 == shift)
        if np.any(mask):
            intensity_matrix_150_300[i, j] = intensity_filtered_150_300[mask][0]

# ---- STEP 3: Create Contour Plot for the second plot ----
plt.figure(figsize=(16, 6))  # Adjust size to fit both plots side by side

# First plot (with the original Raman shift range)
plt.subplot(1, 2, 1)  # Create the first subplot
contour1 = plt.contourf(unique_shifts, unique_times, intensity_matrix, levels=100, cmap="plasma")
plt.ylim([18, max(unique_times)])  # Ensure time is displayed in the right range
plt.gca().invert_yaxis()  # Invert Y-axis if time increases from bottom to top
cbar1 = plt.colorbar(contour1)
cbar1.set_label("Intensity (a.u.)")
plt.xlabel("Raman Shift (cm⁻¹)")
plt.ylabel("Time (hours)")
plt.title("Operando Raman Contour Map (1000-1750 cm⁻¹)")

# Add dashed lines for charge and discharge times (first plot)
for time_point in charge_times:
    plt.axhline(y=time_point, color='red', linestyle='--', linewidth=1)
for time_point in discharge_times:
    plt.axhline(y=time_point, color='blue', linestyle='--', linewidth=1)

# Add labels for Charge and Discharge
for i in range(min(len(charge_times), len(discharge_times))):
    charge_time = charge_times[i]
    discharge_time = discharge_times[i]
    if charge_time < discharge_time:
        midpoint = (charge_time + discharge_time) / 2
        plt.text(
            x=unique_shifts[len(unique_shifts) // 2], y=midpoint,
            s="Charge", color='red', ha='center', va='center', fontsize=12, weight='bold'
        )
        midpoint_next = (discharge_time + charge_times[i + 1]) / 2 if i + 1 < len(charge_times) else discharge_time
        plt.text(
            x=unique_shifts[len(unique_shifts) // 2], y=midpoint_next,
            s="Discharge", color='blue', ha='center', va='center', fontsize=12, weight='bold'
        )

# Second plot (with the truncated Raman shift range)
plt.subplot(1, 2, 2)  # Create the second subplot
contour2 = plt.contourf(unique_shifts_150_300, unique_times_150_300, intensity_matrix_150_300, levels=100, cmap="plasma")
plt.ylim([18, max(unique_times_150_300)])  # Ensure time is displayed in the right range
plt.gca().invert_yaxis()  # Invert Y-axis if time increases from bottom to top
cbar2 = plt.colorbar(contour2)
cbar2.set_label("Intensity (a.u.)")
plt.xlabel("Raman Shift (cm⁻¹)")
plt.ylabel("Time (hours)")
plt.title("Operando Raman Contour Map (150-300 cm⁻¹)")

# Add dashed lines for charge and discharge times (second plot)
for time_point in charge_times:
    plt.axhline(y=time_point, color='red', linestyle='--', linewidth=1)
for time_point in discharge_times:
    plt.axhline(y=time_point, color='blue', linestyle='--', linewidth=1)

# Add labels for Charge and Discharge in the second plot
for i in range(min(len(charge_times), len(discharge_times))):
    charge_time = charge_times[i]
    discharge_time = discharge_times[i]
    if charge_time < discharge_time:
        midpoint = (charge_time + discharge_time) / 2
        plt.text(
            x=unique_shifts_150_300[len(unique_shifts_150_300) // 2], y=midpoint,
            s="Charge", color='red', ha='center', va='center', fontsize=12, weight='bold'
        )
        midpoint_next = (discharge_time + charge_times[i + 1]) / 2 if i + 1 < len(charge_times) else discharge_time
        plt.text(
            x=unique_shifts_150_300[len(unique_shifts_150_300) // 2], y=midpoint_next,
            s="Discharge", color='blue', ha='center', va='center', fontsize=12, weight='bold'
        )

# Show the plot
plt.tight_layout()
plt.show()
