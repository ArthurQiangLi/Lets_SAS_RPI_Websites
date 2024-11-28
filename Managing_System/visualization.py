import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Set the toggle for including Average Latency
include_latency = True  # Set to False to exclude latency from the graph

# Load data from CSV file
file_path = '/mnt/c/Users/danie/Dropbox/bonjr/coding/VSProjects/Lets_SAS_RPI_Websites/Managing_System/system_metrics_latency_attempt.csv'
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

# Extract Average Latency if toggled on
if include_latency:
    average_latency = df['Average Latency (ms)']

# Identify transitions in anomaly labels
transitions = df[df['Anomaly Label'].diff().abs() > 0]

# Plot CPU Usage, Anomaly Label, and optionally Average Latency over time with dual axes
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

# Optionally, add Average Latency to the plot
if include_latency:
    ax3 = ax1.twinx()  # Create a third y-axis
    ax3.spines.right.set_position(("outward", 60))  # Offset the third axis
    ax3.plot(timestamps, average_latency, label="Average Latency (ms)", color="purple", linestyle="--")
    ax3.set_ylabel("Average Latency (ms)", color="purple")
    ax3.tick_params(axis='y', labelcolor="purple")

# Highlight transition points
for idx, row in transitions.iterrows():
    ax1.axvline(x=row['MatplotlibTime'], color='green', linestyle='--', alpha=0.7, label="Transition" if idx == transitions.index[0] else "")

# Combine legends from all axes
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
if include_latency:
    handles3, labels3 = ax3.get_legend_handles_labels()
    handles = handles1 + handles2 + handles3
    labels = labels1 + labels2 + labels3
else:
    handles = handles1 + handles2
    labels = labels1 + labels2
fig.legend(handles, labels, loc="upper left", bbox_to_anchor=(0.1, 0.5))

# Title and layout adjustments
plt.title("CPU Usage, Anomaly Label, and Average Latency Over Time" if include_latency else "CPU Usage and Anomaly Label Over Time")
plt.tight_layout()

# Save the plot as an image file
filename = 'cpu_usage_anomaly_latency_dual_axis.png' if include_latency else 'cpu_usage_anomaly_dual_axis.png'
plt.savefig(filename)
plt.close()

print(f"Plot saved as '{filename}'")
