import joblib
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc
import matplotlib.pyplot as plt

# Load the model, scaler, and encoder
model = joblib.load('isolation_forest_model.pkl')
scaler = joblib.load('scaler.pkl')
encoder = joblib.load('encoder.pkl')

# Load and preprocess data
data = pd.read_csv('/mnt/c/Users/danie/Dropbox/bonjr/coding/VSProjects/Lets_SAS_RPI_Websites/Managing_System/combined.csv')
data['CPU Temp (°C)'] = pd.to_numeric(data['CPU Temp (°C)'], errors='coerce').fillna(0)
weather_encoded = encoder.transform(data[['Weather Description']])
weather_encoded_df = pd.DataFrame(weather_encoded, columns=encoder.get_feature_names_out(['Weather Description']))
data = pd.concat([data.drop(['Weather Description'], axis=1), weather_encoded_df], axis=1)

# Features and labels
features = data.drop(['Timestamp'], axis=1)
X_scaled = scaler.transform(features)

# Generate predictions
y_pred = model.predict(X_scaled)
anomaly_scores = model.decision_function(X_scaled)

# Debug predictions
y_true = [-1 if cpu > 65 or mem > 90 else 1 for cpu, mem in zip(data['CPU Usage (%)'], data['Memory Usage (%)'])]
print("Sample of Ground Truth (y_true):", y_true[:10])
print("Sample of Predictions (y_pred):", y_pred[:10])
print("Sample Anomaly Scores:", anomaly_scores[:10])

# Metrics
precision = precision_score(y_true, y_pred, pos_label=-1)
recall = recall_score(y_true, y_pred, pos_label=-1)
f1 = f1_score(y_true, y_pred, pos_label=-1)
print(f"Precision: {precision:.2f}, Recall: {recall:.2f}, F1 Score: {f1:.2f}")

# Confusion Matrix
cm = confusion_matrix(y_true, y_pred, labels=[-1, 1])
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Anomaly', 'Normal'])
disp.plot(cmap='Blues')
plt.title('Confusion Matrix')
plt.savefig('confusion_matrix.png')  # Save plot
plt.close()

# ROC Curve
fpr, tpr, thresholds = roc_curve(y_true, anomaly_scores, pos_label=-1)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(10, 6))
plt.plot(fpr, tpr, label=f"ROC Curve (AUC = {roc_auc:.2f})", color='blue')
plt.plot([0, 1], [0, 1], linestyle='--', color='red')
plt.title('ROC Curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
plt.savefig('roc_curve.png')  # Save plot
plt.close()
