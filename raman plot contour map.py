import numpy as np
import matplotlib.pyplot as plt

# ---- STEP 1: Load Data ----
file_path = r"C:\Users\StdUser\PycharmProjects\PythonProject\ECEDEC-10-10s-spotparticle-cell5-1sep_Copy.txt" # Change to your actual file path

# Load data (assuming space or tab-separated values, no headers)
data = np.loadtxt(file_path, skiprows=1)

# Extract columns
time = data[:, 0]         # First column → Time (X-axis)
raman_shift = data[:, 1]  # Second column → Raman Shift (Y-axis)
intensity = data[:, 2]    # Third column → Intensity (Z-axis)

# ---- STEP 2: Reshape Data into 2D Grid ----
# Get unique values for the axes
unique_times = np.unique(time)
unique_shifts = np.unique(raman_shift)

# Create a 2D intensity matrix (rows = time, columns = Raman shift)
intensity_matrix = np.zeros((len(unique_times), len(unique_shifts)))

# Fill the matrix by matching (time, Raman Shift) pairs
for i, t in enumerate(unique_times):
    for j, shift in enumerate(unique_shifts):
        mask = (time == t) & (raman_shift == shift)
        if np.any(mask):
            intensity_matrix[i, j] = intensity[mask][0]

# ---- STEP 3: Create Contour Plot ----
plt.figure(figsize=(8, 6))

# Generate contour plot
contour = plt.contourf(unique_shifts, unique_times, intensity_matrix, levels=50, cmap="inferno")

# Add color bar
cbar = plt.colorbar(contour)
cbar.set_label("Intensity (a.u.)")

# 🎯 Highlight Important Raman Peaks (vertical lines)
plt.axvline(x=1600, color="white", linestyle="--", linewidth=1, label="Peak 1600 cm⁻¹")
plt.axvline(x=1320, color="cyan", linestyle=":", linewidth=1, label="Peak 1320 cm⁻¹")
# 🎨 Customize Color Scheme (change cmap)
contour = plt.contourf(unique_shifts, unique_times, intensity_matrix, levels=100, cmap="plasma")

# Labels and title
plt.xlabel("Raman Shift (cm⁻¹)")
plt.ylabel("Time (s) / Voltage (V)")
plt.title("Operando Raman Contour Map")

# Show plot
plt.show()
