import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load data from CSV file
file_path = '/mnt/c/Users/danie/Dropbox/bonjr/coding/VSProjects/Lets_SAS_RPI_Websites/Managing_System/system_metrics.csv'
df = pd.read_csv(file_path)

# Convert 'Timestamp' to datetime and extract only the time part
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df['Time'] = df['Timestamp'].dt.time  # Extract the time part

# Convert time to matplotlib's numeric time format
df['MatplotlibTime'] = mdates.date2num(df['Timestamp'])

# Extract relevant columns for plotting
cpu_usage = df['CPU Usage (%)']
anomaly_label = df['Anomaly Label']
timestamps = df['MatplotlibTime']

# Identify transitions in anomaly labels
transitions = df[df['Anomaly Label'].diff().abs() > 0]

# Plot CPU Usage and Anomaly Label over time with dual axes
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot CPU Usage on the left y-axis
ax1.plot(timestamps, cpu_usage, label="CPU Usage (%)", color="blue", marker="o")
ax1.set_xlabel("Time")
ax1.set_ylabel("CPU Usage (%)", color="blue")
ax1.tick_params(axis='y', labelcolor="blue")
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
ax1.grid()

# Create a secondary y-axis for Anomaly Label
ax2 = ax1.twinx()
ax2.scatter(timestamps, anomaly_label, color="red", label="Anomaly Label")
ax2.set_ylabel("Anomaly Label", color="red")
ax2.tick_params(axis='y', labelcolor="red")

# Set y-axis limits and ticks for anomaly labels
ax2.set_ylim(-1.5, 1.5)
ax2.set_yticks([-1, 1])

# Highlight transition points
for idx, row in transitions.iterrows():
    ax1.axvline(x=row['MatplotlibTime'], color='green', linestyle='--', alpha=0.7, label="Transition" if idx == transitions.index[0] else "")

# Combine legends from both axes
fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.5))

# Title and layout adjustments
plt.title("CPU Usage and Anomaly Label Over Time")
plt.tight_layout()

# Save the plot as an image file
plt.savefig('cpu_usage_anomaly_dual_axis.png')
plt.close()

print("Plot with dual axes saved as 'cpu_usage_anomaly_dual_axis.png'")
