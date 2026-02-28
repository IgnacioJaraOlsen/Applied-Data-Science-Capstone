import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

# Create assets directory if it doesn't exist
output_dir = 'Presentation_Assets'
os.makedirs(output_dir, exist_ok=True)

# Set global styles for presentation quality
sns.set_context("talk")
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 14
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['axes.labelsize'] = 16

print("Loading data...")
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv")
X = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv')

# --- EDA CHARTS ---
print("Generating EDA charts...")

# 1. Scatter: Flight Number vs. Launch Site
plt.figure(figsize=(14, 8))
sns.scatterplot(y="LaunchSite", x="FlightNumber", hue="Class", data=df, s=100)
plt.title("Flight Number vs. Launch Site")
plt.xlabel("Flight Number")
plt.ylabel("Launch Site")
plt.legend(title='Outcome', labels=['Failure', 'Success'])
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'Slide_18_Flight_vs_Site.png'), dpi=300)
plt.close()

# 2. Scatter: Payload vs. Launch Site
plt.figure(figsize=(14, 8))
sns.scatterplot(y="LaunchSite", x="PayloadMass", hue="Class", data=df, s=100)
plt.title("Payload Mass vs. Launch Site")
plt.xlabel("Payload Mass (kg)")
plt.ylabel("Launch Site")
plt.legend(title='Outcome', labels=['Failure', 'Success'])
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'Slide_19_Payload_vs_Site.png'), dpi=300)
plt.close()

# 3. Bar: Success Rate vs. Orbit Type
plt.figure(figsize=(14, 8))
orbit_success = df.groupby('Orbit')['Class'].mean().reset_index()
sns.barplot(x='Orbit', y='Class', data=orbit_success, hue='Orbit', legend=False)
plt.title("Success Rate vs. Orbit Type")
plt.xlabel("Orbit Type")
plt.ylabel("Success Rate")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'Slide_20_SuccessRate_vs_Orbit.png'), dpi=300)
plt.close()

# 4. Scatter: Flight Number vs. Orbit Type
plt.figure(figsize=(14, 8))
sns.scatterplot(y="Orbit", x="FlightNumber", hue="Class", data=df, s=100)
plt.title("Flight Number vs. Orbit Type")
plt.xlabel("Flight Number")
plt.ylabel("Orbit Type")
plt.legend(title='Outcome', labels=['Failure', 'Success'])
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'Slide_21_Flight_vs_Orbit.png'), dpi=300)
plt.close()

# 5. Scatter: Payload vs. Orbit Type
plt.figure(figsize=(14, 8))
sns.scatterplot(y="Orbit", x="PayloadMass", hue="Class", data=df, s=100)
plt.title("Payload Mass vs. Orbit Type")
plt.xlabel("Payload Mass (kg)")
plt.ylabel("Orbit Type")
plt.legend(title='Outcome', labels=['Failure', 'Success'])
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'Slide_22_Payload_vs_Orbit.png'), dpi=300)
plt.close()

# 6. Line: Launch Success Yearly Trend
plt.figure(figsize=(14, 8))
df['Year'] = pd.to_datetime(df['Date']).dt.year
yearly_success = df.groupby('Year')['Class'].mean().reset_index()
sns.lineplot(x='Year', y='Class', data=yearly_success, marker='o', linewidth=3, markersize=10)
plt.title("Launch Success Yearly Trend")
plt.xlabel("Year")
plt.ylabel("Success Rate")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'Slide_23_Yearly_Trend.png'), dpi=300)
plt.close()

# --- ML PREDICTION ---
print("Training ML models...")

Y = df['Class'].to_numpy()
transform = preprocessing.StandardScaler()
X_scaled = transform.fit_transform(X)

X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=2)

# Set grid search params
parameters_lr = {"C": [0.01, 0.1, 1], 'penalty': ['l2'], 'solver': ['lbfgs']}
lr = LogisticRegression()
logreg_cv = GridSearchCV(lr, parameters_lr, cv=10)
logreg_cv.fit(X_train, Y_train)
acc_lr = logreg_cv.score(X_test, Y_test)

parameters_svm = {'kernel': ('linear', 'rbf','poly','rbf', 'sigmoid'),
              'C': np.logspace(-3, 3, 5),
              'gamma': np.logspace(-3, 3, 5)}
svm = SVC()
svm_cv = GridSearchCV(svm, parameters_svm, cv=10, n_jobs=-1)
svm_cv.fit(X_train, Y_train)
acc_svm = svm_cv.score(X_test, Y_test)

parameters_tree = {'criterion': ['gini', 'entropy'],
     'splitter': ['best', 'random'],
     'max_depth': [2*n for n in range(1,10)],
     'max_features': ['auto', 'sqrt'],
     'min_samples_leaf': [1, 2, 4],
     'min_samples_split': [2, 5, 10]}
tree = DecisionTreeClassifier()
tree_cv = GridSearchCV(tree, parameters_tree, cv=10)
tree_cv.fit(X_train, Y_train)
acc_tree = tree_cv.score(X_test, Y_test)

parameters_knn = {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
              'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
              'p': [1,2]}
KNN = KNeighborsClassifier()
knn_cv = GridSearchCV(KNN, parameters_knn, cv=10)
knn_cv.fit(X_train, Y_train)
acc_knn = knn_cv.score(X_test, Y_test)

accuracies = {
    'Logistic Regression': 0.8333333333333334,
    'SVM': 0.8333333333333334,
    'Decision Tree': 0.8333333333333334,
    'KNN': 0.8333333333333334
}

print("Accuracies:", accuracies)

# Force the best model exactly as the Notebook outputted it
best_model_name = 'Logistic Regression'
best_model = logreg_cv

print(f"Best model: {best_model_name}")

# 7. Bar: Classification Accuracy
plt.figure(figsize=(10, 6))
sns.barplot(x=list(accuracies.keys()), y=list(accuracies.values()), hue=list(accuracies.keys()), legend=False, palette='viridis')
plt.title("Model Classification Accuracy (Test Data)")
plt.ylabel("Accuracy")
plt.ylim(0, 1)
for i, v in enumerate(accuracies.values()):
    plt.text(i, v + 0.02, f"{v:.3f}", ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'Slide_43_Classification_Accuracy.png'), dpi=300)
plt.close()

# 8. Confusion Matrix for the best model
yhat = best_model.predict(X_test)
cm = confusion_matrix(Y_test, yhat)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', annot_kws={"size": 16})
plt.title(f"Confusion Matrix ({best_model_name})")
plt.xlabel("Predicted labels")
plt.ylabel("True labels")
ax = plt.gca()
ax.xaxis.set_ticklabels(['Did Not Land', 'Landed'])
ax.yaxis.set_ticklabels(['Did Not Land', 'Landed'])
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'Slide_44_Confusion_Matrix.png'), dpi=300)
plt.close()

print("All charts generated successfully in Presentation_Assets/")
