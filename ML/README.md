# ✈️ Airline Passenger Satisfaction Prediction

Dự án dự đoán mức độ hài lòng của hành khách hàng không sử dụng thuật toán **ID3 Decision Tree** với thư viện **Chefboost**.

## 📋 Mô tả

Ứng dụng web Flask cho phép dự đoán mức độ hài lòng của hành khách dựa trên:
- Thông tin cá nhân (giới tính, độ tuổi, loại khách hàng)
- Thông tin chuyến bay (loại hạng vé, khoảng cách bay)
- Đánh giá dịch vụ (wifi, giải trí, đồ ăn, ghế ngồi, v.v.)
- Tình trạng delay

## 🚀 Cài đặt nhanh

### Cài đặt dependencies
```bash
pip install flask pandas numpy scikit-learn chefboost
```

### Huấn luyện model
```bash
python train_model.py
```

### Chạy ứng dụng
```bash
python app.py
```

Truy cập: http://localhost:5000

## 📦 Cấu trúc dự án

```
hocmaycuoi/
├── app.py                      # Flask application
├── train_model.py              # Model training script
├── train.csv                   # Training data
├── hocmay-ffinal.ipynb         # Original Jupyter notebook
├── templates/
│   └── index.html              # Web interface
├── static/                     # CSS/JS files (if any)
├── label_encoders.pkl          # (Generated) Label encoders
├── binning_config.pkl          # (Generated) Binning configuration
├── feature_columns.pkl         # (Generated) Feature column names
├── id3_model.pkl              # (Generated) Trained model
└── outputs/                    # (Generated) Chefboost model files
```

## 🧠 Mô hình

**Thuật toán:** ID3 (Iterative Dichotomiser 3)  
**Thư viện:** Chefboost  
**Độ chính xác:** ~89-90%

### Tiền xử lý dữ liệu

1. **Binning (Gom nhóm):**
   - Tuổi: `<20, 20-29, 30-39, 40-49, 50-59, 60+`
   - Khoảng cách bay: `0-500, 501-1000, 1001-1500, 1501-2000, 2001-2500, 2500+`
   - Delay: `On time, Slightly delayed, Moderately delayed, Delayed, Very delayed`

2. **Label Encoding:** 
   - Tất cả biến phân loại được mã hóa thành số

3. **Train/Test Split:** 80/20

## 💡 Sử dụng

1. Mở trình duyệt tại `http://localhost:5000`
2. Điền thông tin hành khách vào form
3. Đánh giá các dịch vụ bằng hệ thống sao (1-5 sao)
4. Nhập thời gian delay (nếu có)
5. Click "PREDICT CUSTOMER SATISFACTION"
6. Xem kết quả dự đoán

## 📊 Đầu vào

### Thông tin hành khách
- Gender (Giới tính)
- Customer Type (Loại khách hàng)
- Age (Tuổi)
- Type of Travel (Mục đích di chuyển)
- Class (Hạng vé)
- Flight Distance (Khoảng cách bay)

### Đánh giá dịch vụ (1-5 sao)
- Inflight Wifi Service
- Departure/Arrival Time Convenient
- Ease of Online Booking
- Gate Location
- Food and Drink
- Online Boarding
- Seat Comfort
- Inflight Entertainment
- On-board Service
- Leg Room Service
- Baggage Handling
- Check-in Service
- Inflight Service
- Cleanliness

### Delay
- Departure Delay (phút)
- Arrival Delay (phút)

## 📈 Đầu ra

Kết quả dự đoán:
- ✅ **PASSENGER SATISFIED** (Hành khách hài lòng)
- ❌ **PASSENGER DISSATISFIED** (Hành khách không hài lòng)

## 🛠️ Công nghệ

- **Backend:** Flask (Python)
- **Machine Learning:** ID3 Decision Tree (Chefboost)
- **Preprocessing:** Pandas, NumPy, Scikit-learn
- **Frontend:** HTML, CSS (Bootstrap), JavaScript
- **UI/UX:** Gradient design, star ratings, animations

## 📝 Lưu ý

- Cần chạy `train_model.py` ít nhất 1 lần trước khi chạy `app.py`
- File `train.csv` phải có mặt trong thư mục dự án
- Model training có thể mất vài phút (tùy thuộc vào kích thước dữ liệu)
- Chefboost tự động lưu model vào thư mục `outputs/`

## 🔧 Troubleshooting

### Lỗi: "Model not loaded"
```bash
# Chạy lại train_model.py
python train_model.py
```

### Lỗi: "chefboost not installed"
```bash
pip install chefboost
```

### Lỗi: "train.csv not found"
Đảm bảo file `train.csv` có trong cùng thư mục với `train_model.py`

## 📚 Tham khảo

- [Chefboost Documentation](https://github.com/serengil/chefboost)
- [ID3 Algorithm](https://en.wikipedia.org/wiki/ID3_algorithm)
- Jupyter Notebook gốc: `hocmay-ffinal.ipynb`

## 👨‍💻 Tác giả

Dự án học máy - Dự đoán mức độ hài lòng khách hàng hàng không

---

Made with ❤️ using Python & Flask
