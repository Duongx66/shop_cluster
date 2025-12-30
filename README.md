# 📦 Customer Segmentation from Association Rules

Dự án này tập trung vào việc **kết hợp khai phá luật kết hợp (Association Rule Mining)** và  
**phân cụm khách hàng (Clustering)** nhằm chuyển dữ liệu giao dịch bán lẻ thành  
**các phân khúc khách hàng có ý nghĩa hành động cho marketing**.

Pipeline được xây dựng theo hướng:
**Luật kết hợp → Đặc trưng hành vi → Phân cụm → Diễn giải → Chiến lược marketing**

---

## 👥 Thông tin Nhóm
- **Nhóm:** …
- **Thành viên:**
  - Nguyễn Đức Dương
  - Nguyễn Mạnh Cường
  - Nguyễn Đoàn Ngọc Linh
- **Môn học:** Data Mining  
- **Giảng viên:** Lê Thị Thùy Trang
- **Dataset:** Online Retail (UCI Machine Learning Repository)

---

## 🎯 Mục tiêu Dự án
Sau khi hoàn thành dự án, nhóm có thể:
1. Hiểu quy trình kết hợp giữa **khai phá luật** và **phân cụm**.
2. Trích xuất đặc trưng hành vi từ **luật kết hợp**.
3. Áp dụng các thuật toán phân cụm (K-Means, mở rộng).
4. Trực quan hóa và diễn giải các cụm khách hàng.
5. Đề xuất **chiến lược marketing cụ thể** cho từng phân khúc.

---

## 🔁 Pipeline Thực hiện

1. **Tiền xử lý & Khai phá luật**
   - Làm sạch dữ liệu giao dịch
   - Sinh luật bằng Apriori / FP-Growth
   - Lọc luật theo `support`, `confidence`, `lift`

2. **Rule-based Feature Engineering**
   - Mỗi luật tương ứng một feature
   - Khách hàng thỏa antecedent → kích hoạt feature
   - Hỗ trợ:
     - Feature nhị phân
     - Feature có trọng số (lift / lift × confidence)

3. **Ghép RFM (Tuỳ chọn)**
   - Recency – Frequency – Monetary
   - Chuẩn hóa dữ liệu để tạo vector đặc trưng cuối

4. **Phân cụm khách hàng**
   - Thuật toán: K-Means
   - Chọn số cụm K bằng Silhouette / Elbow

5. **Trực quan hóa & Diễn giải**
   - Giảm chiều bằng PCA / SVD
   - Profiling cụm theo:
     - Quy mô
     - RFM
     - Luật nổi bật

6. **Đề xuất chiến lược marketing**
   - Cross-sell / Bundle
   - Upsell
   - Chăm sóc VIP
   - Kích hoạt khách hàng ngủ đông

---

## 🧩 Feature Engineering Strategy

### 🔹 Baseline
- Feature nhị phân theo luật
- 1 = khách hàng thỏa luật
- 0 = không thỏa

### 🔹 Nâng cao
- Feature luật có trọng số (lift hoặc lift × confidence)
- Ghép thêm RFM
- Chuẩn hóa dữ liệu trước phân cụm

👉 Thực hiện **so sánh có hệ thống** giữa các cấu hình:
- Rule-only vs Rule + RFM
- Binary vs Weighted rules
- Top-K luật nhỏ vs lớn

---

## 📊 Đánh giá & Trực quan hóa

- Chọn K bằng **Silhouette Score**
- Scatter plot 2D (PCA / SVD)
- Nhận xét mức độ tách cụm và chồng lấn

---

## 🧠 Profiling & Insight Kinh doanh

Mỗi cụm được phân tích theo:
- Số lượng khách hàng
- Trung bình / trung vị RFM
- Top luật được kích hoạt nhiều nhất

Từ đó:
- Đặt tên cụm (EN + VI)
- Mô tả persona (1 câu)
- Đề xuất chiến lược marketing phù hợp

---

## 🖥️ Dashboard (Streamlit)

- Đọc file output phân cụm
- Lọc theo cluster
- Xem top rules theo cụm
- Gợi ý bundle / cross-sell

---

## 📂 Cấu trúc Project

```text
DATAMINING/
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── clustering_from_rules.ipynb
│
├── src/
│   └── cluster_library.py
│
├── dashboard/
│   └── app.py
│
├── requirements.txt
└── README.md
