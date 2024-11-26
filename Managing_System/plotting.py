import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
file_path_adaptation_on = 'Managing_System/system_metrics_graph_attempt_2.csv'
file_path_adaptation_off = 'Managing_System/system_metrics_graph_attempt_3.csv'

data_adaptation_on = pd.read_csv(file_path_adaptation_on)
data_adaptation_off = pd.read_csv(file_path_adaptation_off)

# Convert 'Timestamp' to datetime objects for proper plotting
data_adaptation_on['Timestamp'] = pd.to_datetime(data_adaptation_on['Timestamp'])
data_adaptation_off['Timestamp'] = pd.to_datetime(data_adaptation_off['Timestamp'])

# Align timestamps
start_time_on = data_adaptation_on['Timestamp'].iloc[0]
start_time_off = data_adaptation_off['Timestamp'].iloc[0]
time_difference = start_time_on - start_time_off

# Adjust timestamps in the 'off' dataset to match the 'on' dataset
data_adaptation_off['Adjusted Timestamp'] = data_adaptation_off['Timestamp'] + time_difference

# Check if data spans multiple dates
unique_dates_on = data_adaptation_on['Timestamp'].dt.date.unique()
unique_dates_off = data_adaptation_off['Adjusted Timestamp'].dt.date.unique()
unique_dates = set(unique_dates_on).union(set(unique_dates_off))

# Determine the x-axis format based on the number of unique dates
if len(unique_dates) == 1:
    # Single date: show only time
    x_format = '%H:%M:%S'
else:
    # Multiple dates: show date and time
    x_format = '%Y-%m-%d %H:%M:%S'

# Plot the data with a square layout
plt.figure(figsize=(8, 8))  # Square dimensions

# Plot adaptation on and off data
plt.plot(data_adaptation_on['Timestamp'], data_adaptation_on['CPU Usage (%)'], 
         label='Adaptation On', linestyle='--', color='blue', linewidth=1.5)
plt.plot(data_adaptation_off['Adjusted Timestamp'], data_adaptation_off['CPU Usage (%)'], 
         label='Adaptation Off', linestyle='-', color='red', linewidth=1.5)

# Add title, labels, legend, and grid
title_size = 16
axis_label_size = 14

plt.title('CPU Usage Over Time: Adaptation On vs Off (Aligned)', fontsize=title_size)
plt.xlabel('Time', fontsize=axis_label_size)
plt.ylabel('CPU Usage (%)', fontsize=axis_label_size)

# Format the x-axis labels
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter(x_format))
plt.xticks(fontsize=10, rotation=0)

plt.grid(alpha=0.5)
plt.legend(fontsize=12, loc='upper left')

# Adjust layout to make it look neat
plt.tight_layout()

# Save the plot to a file
plt.savefig("cpu_usage_comparison_on_off.png")

# Display the plot
# plt.show()
#