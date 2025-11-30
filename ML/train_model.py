"""
Train Airline Passenger Satisfaction Model using ID3 Algorithm (Chefboost)
Based on hocmay-ffinal.ipynb
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle
import warnings

warnings.filterwarnings('ignore')

print("=" * 60)
print("🚀 TRAINING AIRLINE PASSENGER SATISFACTION MODEL (ID3)")
print("=" * 60)

# ==========================================
# 1. LOAD DATA
# ==========================================
print("\n📂 Loading data...")
try:
    df = pd.read_csv('train.csv')
    print(f"✅ Loaded {len(df)} records from train.csv")
except FileNotFoundError:
    print("❌ Error: train.csv not found!")
    exit(1)

# ==========================================
# 2. DATA CLEANING
# ==========================================
print("\n🧹 Cleaning data...")
drop_cols = ['id', 'Unnamed: 0']
df = df.drop(columns=[c for c in drop_cols if c in df.columns])
df = df.dropna()
print(f"✅ Data cleaned. {len(df)} records remaining")

# ==========================================
# 3. BINNING (GROUPING)
# ==========================================
print("\n📊 Binning data...")

# a. Age
bins_age = [0, 19, 29, 39, 49, 59, 120]
labels_age = ['<20', '20-29', '30-39', '40-49', '50-59', '60+']
df['Age'] = pd.cut(df['Age'], bins=bins_age, labels=labels_age)

# b. Delay times
bins_delay = [-1, 0, 5, 15, 30, 100000]
labels_delay = ['On time', 'Slightly delayed', 'Moderately delayed', 'Delayed', 'Very delayed']

df['Arrival Delay in Minutes'] = pd.cut(df['Arrival Delay in Minutes'], bins=bins_delay, labels=labels_delay)
df['Departure Delay in Minutes'] = pd.cut(df['Departure Delay in Minutes'], bins=bins_delay, labels=labels_delay)

# c. Flight Distance
bins_dist = [0, 500, 1000, 1500, 2000, 2500, df['Flight Distance'].max() + 1]
labels_dist = ['0-500', '501-1000', '1001-1500', '1501-2000', '2001-2500', '2500+']
df['Flight Distance'] = pd.cut(df['Flight Distance'], bins=bins_dist, labels=labels_dist)

print("✅ Binning complete")

# ==========================================
# 4. LABEL ENCODING
# ==========================================
print("\n🔢 Encoding categorical variables...")

cat_cols = ['Gender', 'Customer Type', 'Age', 'Type of Travel', 'Class',
            'Departure Delay in Minutes', 'Arrival Delay in Minutes',
            'satisfaction', 'Flight Distance']

label_encoders = {}
for col in cat_cols:
    le = LabelEncoder()
    df[col] = df[col].astype(str)
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

print("✅ Encoding complete")

# Save label encoders
with open('label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)
print("💾 Saved label_encoders.pkl")

# Save binning configurations
binning_config = {
    'bins_age': bins_age,
    'labels_age': labels_age,
    'bins_delay': bins_delay,
    'labels_delay': labels_delay,
    'bins_dist': bins_dist,
    'labels_dist': labels_dist
}
with open('binning_config.pkl', 'wb') as f:
    pickle.dump(binning_config, f)
print("💾 Saved binning_config.pkl")

# ==========================================
# 5. TRAIN/TEST SPLIT
# ==========================================
print("\n✂️ Splitting data...")
X = df.drop(columns=['satisfaction'])
y = df['satisfaction']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Prepare for Chefboost
df_train = X_train.copy()
df_train['satisfaction'] = y_train
df_train['satisfaction'] = df_train['satisfaction'].astype(str)

print(f"✅ Train set: {len(df_train)} records")
print(f"✅ Test set: {len(X_test)} records")

# Save column names for prediction
feature_columns = X_train.columns.tolist()
with open('feature_columns.pkl', 'wb') as f:
    pickle.dump(feature_columns, f)
print("💾 Saved feature_columns.pkl")

# ==========================================
# 6. TRAIN ID3 MODEL (CHEFBOOST)
# ==========================================
print("\n🌳 Training ID3 model with Chefboost...")
print("⏳ This may take a while... Please wait...")

try:
    from chefboost import Chefboost as cb
    
    config = {
        'algorithm': 'ID3',
        'enableParallelism': False  # Disabled for Windows compatibility
    }
    
    model = cb.fit(df_train, config=config, target_label='satisfaction')
    print("✅ ID3 model training complete!")
    
    # The model is saved automatically by chefboost in 'outputs' folder
    # We also save the model object
    with open('id3_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("💾 Saved id3_model.pkl")
    
except ImportError:
    print("❌ Error: chefboost not installed!")
    print("📦 Please install it using: pip install chefboost")
    exit(1)
except Exception as e:
    print(f"❌ Error during training: {e}")
    exit(1)

# ==========================================
# 7. EVALUATE MODEL
# ==========================================
print("\n📈 Evaluating model on test set...")

y_pred_list = []
for index, row in X_test.iterrows():
    instance = row[feature_columns].tolist()
    prediction = cb.predict(model, instance)
    y_pred_list.append(prediction)

y_pred_numeric = [int(p) for p in y_pred_list]

accuracy = accuracy_score(y_test, y_pred_numeric)
print("\n" + "=" * 60)
print("📊 MODEL EVALUATION RESULTS")
print("=" * 60)
print(f"✅ Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
print("\n📋 Classification Report:")
print(classification_report(y_test, y_pred_numeric))

print("\n" + "=" * 60)
print("✅ TRAINING COMPLETE!")
print("=" * 60)
print("📁 Files saved:")
print("   - label_encoders.pkl")
print("   - binning_config.pkl")
print("   - feature_columns.pkl")
print("   - id3_model.pkl")
print("   - outputs/ (chefboost model files)")
print("\n🚀 You can now run: python app.py")
print("=" * 60)
