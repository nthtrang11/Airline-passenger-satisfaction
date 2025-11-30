"""
Flask Web Application for Airline Passenger Satisfaction Prediction
Using ID3 Decision Tree Model (Chefboost)
"""

from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np
import warnings
import os
import sys

warnings.filterwarnings('ignore')

app = Flask(__name__)

# ==========================================
# LOAD MODEL AND ENCODERS
# ==========================================
try:
    with open('label_encoders.pkl', 'rb') as f:
        label_encoders = pickle.load(f)
    
    with open('binning_config.pkl', 'rb') as f:
        binning_config = pickle.load(f)
    
    with open('feature_columns.pkl', 'rb') as f:
        feature_columns = pickle.load(f)
    
    with open('id3_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    from chefboost import Chefboost as cb
    
    print("\n" + "=" * 50)
    print("🛫 APPLICATION DỰ ĐOÁN MỨCDỘ HÀI LÒNG KHÁCH HÀNG HÀNG KHÔNG")
    print("=" * 50)
    print("\n✅ Model loaded successfully!")
    print(f"✅ Features: {len(feature_columns)} columns")
    print(f"✅ Encoders: {len(label_encoders)} categorical variables")
    
except FileNotFoundError as e:
    print(f"\n❌ Lỗi khi load model: {e}")
    print("⚠️  Vui lòng chạy train_model.py trước!")
    print("\n" + "=" * 50)
    print("🛫 APPLICATION DỰ ĐOÁN MỨCDỘ HÀI LÒNG KHÁCH HÀNG HÀNG KHÔNG")
    print("=" * 50)
    label_encoders = None
    binning_config = None
    feature_columns = None
    model = None

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def apply_age_binning(age):
    """Apply age binning"""
    bins = binning_config['bins_age']
    labels = binning_config['labels_age']
    
    for i in range(len(bins) - 1):
        if bins[i] <= age < bins[i + 1]:
            return labels[i]
    return labels[-1]

def apply_delay_binning(delay):
    """Apply delay binning"""
    bins = binning_config['bins_delay']
    labels = binning_config['labels_delay']
    
    for i in range(len(bins) - 1):
        if bins[i] < delay <= bins[i + 1]:
            return labels[i]
    return labels[-1]

def apply_distance_binning(distance):
    """Apply flight distance binning"""
    bins = binning_config['bins_dist']
    labels = binning_config['labels_dist']
    
    for i in range(len(bins) - 1):
        if bins[i] <= distance < bins[i + 1]:
            return labels[i]
    return labels[-1]

# ==========================================
# ROUTES
# ==========================================
@app.route('/')
def index():
    """Render home page with form"""
    # Get unique values for dropdowns from label encoders
    if label_encoders:
        genders = label_encoders['Gender'].classes_
        customer_types = label_encoders['Customer Type'].classes_
        travel_types = label_encoders['Type of Travel'].classes_
        classes = label_encoders['Class'].classes_
    else:
        # Default values if model not loaded
        genders = ['Male', 'Female']
        customer_types = ['Loyal Customer', 'disloyal Customer']
        travel_types = ['Business travel', 'Personal Travel']
        classes = ['Business', 'Eco', 'Eco Plus']
    
    return render_template('index.html',
                         genders=genders,
                         customer_types=customer_types,
                         travel_types=travel_types,
                         classes=classes)

@app.route('/predict', methods=['POST'])
def predict():
    """Make prediction based on form data"""
    try:
        if not model:
            return jsonify({
                'success': False,
                'error': 'Model not loaded. Please run train_model.py first!'
            })
        
        # Get form data
        data = request.json
        
        # Extract values
        gender = data['gender']
        customer_type = data['customerType']
        age = int(data['age'])
        travel_type = data['travelType']
        class_ = data['class']
        distance = int(data['distance'])
        
        wifi = int(data['wifi'])
        time_conv = int(data['timeConv'])
        booking = int(data['booking'])
        gate = int(data['gate'])
        food = int(data['food'])
        boarding = int(data['boarding'])
        seat = int(data['seat'])
        entertainment = int(data['entertainment'])
        onboard = int(data['onboard'])
        legroom = int(data['legroom'])
        baggage = int(data['baggage'])
        checkin = int(data['checkin'])
        service = int(data['service'])
        cleanliness = int(data['cleanliness'])
        
        dep_delay = int(data['depDelay'])
        arr_delay = int(data['arrDelay'])
        
        # Apply binning
        age_binned = apply_age_binning(age)
        distance_binned = apply_distance_binning(distance)
        dep_delay_binned = apply_delay_binning(dep_delay)
        arr_delay_binned = apply_delay_binning(arr_delay)
        
        # Create input dictionary
        sample_input = {
            'Gender': gender,
            'Customer Type': customer_type,
            'Age': age_binned,
            'Type of Travel': travel_type,
            'Class': class_,
            'Flight Distance': distance_binned,
            'Inflight wifi service': wifi,
            'Departure/Arrival time convenient': time_conv,
            'Ease of Online booking': booking,
            'Gate location': gate,
            'Food and drink': food,
            'Online boarding': boarding,
            'Seat comfort': seat,
            'Inflight entertainment': entertainment,
            'On-board service': onboard,
            'Leg room service': legroom,
            'Baggage handling': baggage,
            'Checkin service': checkin,
            'Inflight service': service,
            'Cleanliness': cleanliness,
            'Departure Delay in Minutes': dep_delay_binned,
            'Arrival Delay in Minutes': arr_delay_binned
        }
        
        # Encode input
        encoded_sample = []
        for col in feature_columns:
            val = sample_input.get(col)
            if col in label_encoders:
                val_encoded = label_encoders[col].transform([str(val)])[0]
                encoded_sample.append(val_encoded)
            else:
                encoded_sample.append(val)
        
        # Make prediction
        pred_val = cb.predict(model, encoded_sample)
        
        # Decode result
        final_result = label_encoders['satisfaction'].inverse_transform([int(pred_val)])[0]
        
        # Check if satisfied
        is_satisfied = final_result.lower() == 'satisfied'
        
        return jsonify({
            'success': True,
            'satisfied': is_satisfied,
            'prediction': final_result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# ==========================================
# MAIN
# ==========================================
if __name__ == '__main__':
    print("\n✈️  Server đang chạy tại: http://localhost:5000")
    print("📊 Nhấn Ctrl+C để dừng server\n")
    
    # Configure to ignore outputs directory from auto-reload
    extra_dirs = ['templates', 'static']
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in os.walk(extra_dir):
            # Ignore outputs directory
            if 'outputs' in dirs:
                dirs.remove('outputs')
            for filename in files:
                filename = os.path.join(dirname, filename)
                if os.path.isfile(filename):
                    extra_files.append(filename)
    
    app.run(debug=True, port=5000, extra_files=extra_files, use_reloader=True)
