"""
Flask Web Application for Airline Passenger Satisfaction Prediction
Using ok
"""

from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np
import warnings
import os

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
    
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    print("\n" + "=" * 50)
    print("🛫 APPLICATION DỰ ĐOÁN MỨCDỘ HÀI LÒNG KHÁCH HÀNG HÀNG KHÔNG")
    print("=" * 50)
    print("\n✅ Model loaded successfully!")
    print(f"✅ Features: {len(feature_columns)} columns")
    print(f"✅ Encoders: {len(label_encoders)} categorical variables")
    
except FileNotFoundError as e:
    print(f"\n❌ Lỗi khi load model: {e}")
    print("⚠️  Vui lòng chạy train_model_fast.py trước!")
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

def find_main_reason(row, prediction):
    """Find main reason for dissatisfaction based on lowest service ratings"""
    service_features = {
        'Inflight wifi service': 'Wifi',
        'Departure/Arrival time convenient': 'Time Convenience',
        'Ease of Online booking': 'Online Booking',
        'Gate location': 'Gate Location',
        'Food and drink': 'Food & Drink',
        'Online boarding': 'Online Boarding',
        'Seat comfort': 'Seat Comfort',
        'Inflight entertainment': 'Entertainment',
        'On-board service': 'Onboard Service',
        'Leg room service': 'Leg Room',
        'Baggage handling': 'Baggage',
        'Checkin service': 'Check-in',
        'Inflight service': 'Inflight Service',
        'Cleanliness': 'Cleanliness'
    }
    
    if prediction == 'neutral or dissatisfied':
        # Find services with rating <= 2
        poor_services = []
        for feature, display_name in service_features.items():
            if feature in row and row[feature] <= 2:
                poor_services.append((display_name, row[feature]))
        
        if poor_services:
            # Sort by rating (lowest first)
            poor_services.sort(key=lambda x: x[1])
            # Return up to 2 worst services
            reasons = [s[0] for s in poor_services[:2]]
            return ', '.join(reasons)
        else:
            # Check delays
            if 'Departure Delay in Minutes' in row and row['Departure Delay in Minutes'] > 30:
                return 'Departure Delay'
            elif 'Arrival Delay in Minutes' in row and row['Arrival Delay in Minutes'] > 30:
                return 'Arrival Delay'
            return 'Multiple Factors'
    else:
        # For satisfied customers, find highest rated services
        good_services = []
        for feature, display_name in service_features.items():
            if feature in row and row[feature] >= 4:
                good_services.append((display_name, row[feature]))
        
        if good_services:
            good_services.sort(key=lambda x: x[1], reverse=True)
            reasons = [s[0] for s in good_services[:2]]
            return ', '.join(reasons)
        return 'Overall Experience'

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
                'error': 'Model not loaded. Please run train_model_fast.py first!'
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
        pred_val = model.predict([encoded_sample])[0]
        
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

@app.route('/predict_batch', methods=['POST'])
def predict_batch():
    """Make batch predictions from uploaded CSV file"""
    try:
        if not model:
            return jsonify({
                'success': False,
                'error': 'Model not loaded. Please run train_model_fast.py first!'
            })
        
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            })
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            })
        
        # Read CSV file
        df = pd.read_csv(file)
        
        # Store original data for display
        original_df = df.copy()
        
        # Required columns
        required_cols = [
            'Gender', 'Customer Type', 'Age', 'Type of Travel', 'Class',
            'Flight Distance', 'Inflight wifi service', 
            'Departure/Arrival time convenient', 'Ease of Online booking',
            'Gate location', 'Food and drink', 'Online boarding',
            'Seat comfort', 'Inflight entertainment', 'On-board service',
            'Leg room service', 'Baggage handling', 'Checkin service',
            'Inflight service', 'Cleanliness', 
            'Departure Delay in Minutes', 'Arrival Delay in Minutes'
        ]
        
        # Check if all required columns exist
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            return jsonify({
                'success': False,
                'error': f'Missing columns: {", ".join(missing_cols)}'
            })
        
        # Process each row
        predictions = []
        
        for idx, row in df.iterrows():
            try:
                # Apply binning
                age_binned = apply_age_binning(row['Age'])
                distance_binned = apply_distance_binning(row['Flight Distance'])
                dep_delay_binned = apply_delay_binning(row['Departure Delay in Minutes'])
                arr_delay_binned = apply_delay_binning(row['Arrival Delay in Minutes'])
                
                # Create input dictionary
                sample_input = {
                    'Gender': row['Gender'],
                    'Customer Type': row['Customer Type'],
                    'Age': age_binned,
                    'Type of Travel': row['Type of Travel'],
                    'Class': row['Class'],
                    'Flight Distance': distance_binned,
                    'Inflight wifi service': row['Inflight wifi service'],
                    'Departure/Arrival time convenient': row['Departure/Arrival time convenient'],
                    'Ease of Online booking': row['Ease of Online booking'],
                    'Gate location': row['Gate location'],
                    'Food and drink': row['Food and drink'],
                    'Online boarding': row['Online boarding'],
                    'Seat comfort': row['Seat comfort'],
                    'Inflight entertainment': row['Inflight entertainment'],
                    'On-board service': row['On-board service'],
                    'Leg room service': row['Leg room service'],
                    'Baggage handling': row['Baggage handling'],
                    'Checkin service': row['Checkin service'],
                    'Inflight service': row['Inflight service'],
                    'Cleanliness': row['Cleanliness'],
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
                pred_val = model.predict([encoded_sample])[0]
                final_result = label_encoders['satisfaction'].inverse_transform([int(pred_val)])[0]
                
                # Find main reason for the prediction
                main_reason = find_main_reason(row, final_result)
                
                predictions.append({
                    'result': final_result,
                    'reason': main_reason
                })
                
            except Exception as e:
                predictions.append({
                    'result': f'Error: {str(e)}',
                    'reason': 'N/A'
                })
        
        # Add predictions to dataframe
        original_df['Prediction'] = [p['result'] for p in predictions]
        original_df['Main Reason'] = [p['reason'] for p in predictions]
        
        # Calculate statistics
        satisfied_count = sum(1 for p in predictions if p['result'] == 'satisfied')
        dissatisfied_count = sum(1 for p in predictions if p['result'] == 'neutral or dissatisfied')
        error_count = sum(1 for p in predictions if str(p['result']).startswith('Error'))
        
        total = len(predictions)
        satisfied_pct = (satisfied_count / total * 100) if total > 0 else 0
        dissatisfied_pct = (dissatisfied_count / total * 100) if total > 0 else 0
        
        # Convert dataframe to dict for JSON response
        results_data = original_df.head(100).to_dict('records')  # Limit to first 100 for display
        
        return jsonify({
            'success': True,
            'total': total,
            'satisfied': satisfied_count,
            'dissatisfied': dissatisfied_count,
            'errors': error_count,
            'satisfied_percentage': round(satisfied_pct, 2),
            'dissatisfied_percentage': round(dissatisfied_pct, 2),
            'results': results_data,
            'showing': min(100, total)
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
    app.run(debug=True, port=5000)
