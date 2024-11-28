import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Load live system data
data = pd.read_csv('/mnt/c/Users/danie/Dropbox/bonjr/coding/VSProjects/Lets_SAS_RPI_Websites/Managing_System/system_metrics.csv')

# Ensure the 'Timestamp' column is parsed as datetime for proper plotting
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# Extract labels and predictions
y_true = data['Anomaly Label']  # Replace with ground truth if available
y_pred = data['Anomaly Label']  # Currently using the same column as predictions (adjust as needed)

# Confusion Matrix
# Since both `y_true` and `y_pred` are the same, the confusion matrix will only show diagonal elements.
cm = confusion_matrix(y_true, y_pred, labels=[-1, 1])
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Anomaly', 'Normal'])
disp.plot(cmap='Blues')
plt.title('Confusion Matrix (Live Data)')
plt.savefig('confusion_matrix_live_data.png')  # Save plot instead of displaying directly
plt.close()

# Anomaly Score Distribution (e.g., for Average Latency)
plt.figure(figsize=(10, 6))
sns.histplot(data['Average Latency (ms)'], kde=True, bins=50, color='blue')
plt.title('Latency Distribution (Live Data)')
plt.xlabel('Average Latency (ms)')
plt.ylabel('Frequency')
plt.savefig('latency_distribution_live_data.png')  # Save plot instead of displaying directly
plt.close()

# Threshold Adaptations Over Time
plt.figure(figsize=(10, 6))
plt.plot(data['Timestamp'], data['CPU Threshold Upper'], label='CPU Threshold Upper', color='red')
plt.plot(data['Timestamp'], data['Memory Threshold Upper'], label='Memory Threshold Upper', color='green')
plt.xticks(rotation=45)
plt.title('Threshold Adaptations Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Threshold (%)')
plt.legend()
plt.savefig('threshold_adaptations_over_time.png')  # Save plot instead of displaying directly
plt.close()
