# 📦 Shopping Cart Analysis & Case Study

Dự án phân tích dữ liệu bán lẻ nhằm khám phá mối quan hệ giữa các sản phẩm thường được mua cùng nhau, sử dụng kỹ thuật **Association Rule Mining (Apriori)**.  
Project triển khai pipeline đầy đủ từ **xử lý dữ liệu → phân tích → khai thác luật → trực quan hóa → insight kinh doanh**.

---

## 👥 Thông tin Nhóm
- **Nhóm:** Nhóm 9
- **Thành viên:**
  - Trần Trường Giang
  - Lưu Khoa Bằng
  - Nguyễn Đức Dương
- **Chủ đề :** **5.3.2.3 – Đánh giá luật theo Lift và giá trị kinh doanh**
  - Xếp hạng luật theo Lift
  - Phân loại luật theo Support / Confidence / Lift
  - Đề xuất chiến lược marketing tương ứng
- **Dataset:** Online Retail (UCI Machine Learning Repository)

---

## 🎯 Mục tiêu
Hiểu rõ hành vi mua sắm của khách hàng, từ đó:
- Phát hiện các cặp sản phẩm thường được mua cùng nhau
- Hỗ trợ tạo combo & gợi ý mua kèm (cross-selling)
- Cá nhân hóa marketing
- Tối ưu bố trí sản phẩm trong cửa hàng
- Gia tăng giá trị giỏ hàng

---

## 📝 Quy trình Thực hiện
1. Làm sạch dữ liệu & xử lý giá trị lỗi
2. Xây dựng **basket matrix (transaction × product)**
3. Khai phá **Frequent Itemsets**
4. Sinh **Association Rules** bằng Apriori
5. Trực quan hóa kết quả
6. Phân tích insight & đề xuất hành động kinh doanh

---

## 🧹 Tiền xử lý Dữ liệu

**Các bước làm sạch chính:**
- Loại bỏ sản phẩm không có mô tả
- Loại bỏ hóa đơn bị hủy (`InvoiceNo` bắt đầu bằng `"C"`)
- Loại bỏ giao dịch có `Quantity ≤ 0` hoặc `UnitPrice ≤ 0`

**Thống kê sau tiền xử lý (UK):**
- Số giao dịch: **~397,924**
- Số sản phẩm duy nhất: **~4,372**
- Số khách hàng: **~4,372**

---

## 🔍 Áp dụng Thuật toán Apriori

**Tham số sử dụng:**
- `min_support = 0.01`
- `min_confidence = 0.3`
- `min_lift = 1.2`

**Kết quả:**
- Tổng số luật sinh ra: **218**
- Số luật sau lọc: **175**
  - Đáp ứng đồng thời Support, Confidence và Lift

---

## 📊 Trực quan hóa Kết quả

### 📌 Biểu đồ 1 – Top 10 luật theo Lift
*(Thay bằng hình ảnh trong báo cáo / notebook)*

**Ý nghĩa:**
- Lift cao cho thấy các sản phẩm được mua cùng nhau **nhiều hơn đáng kể so với ngẫu nhiên**
- Phù hợp để:
  - Tạo combo
  - Gợi ý mua kèm
  - Sắp xếp sản phẩm gần nhau

---

### 📌 Biểu đồ 2 – Scatter plot: Support vs Confidence
*(Thay bằng hình ảnh trong báo cáo / notebook)*

**Ý nghĩa:**
- **Support cao + Confidence cao:** luật phổ biến, đáng tin cậy → áp dụng rộng
- **Lift cao nhưng Support thấp:** luật mạnh nhưng niche → marketing cá nhân hóa

---

## 💡 Insight Kinh doanh

### 1️⃣ Tạo combo từ các luật Lift cao
- **Luật:**  
  `ROSES REGENCY TEACUP AND SAUCER → GREEN REGENCY TEACUP AND SAUCER`
- **Chỉ số:**  
  Lift = 14.16 | Confidence = 0.73 | Support = 0.0388
- **Hành động:**  
  Tạo combo 2 sản phẩm, bày cạnh nhau trên kệ.

---

### 2️⃣ Gợi ý mua thêm dựa trên Confidence cao
- **Luật:**  
  `GREEN REGENCY TEACUP AND SAUCER → ROSES REGENCY TEACUP AND SAUCER`
- **Chỉ số:**  
  Confidence = 0.75 | Lift = 14.16
- **Hành động:**  
  Gợi ý mua thêm qua POS, email, hoặc app bán hàng.

---

### 3️⃣ Nhận diện sản phẩm phổ biến trong giỏ hàng
- **Luật:**  
  `JUMBO BAG RED RETROSPOT → JUMBO BAG PINK POLKADOT`
- **Chỉ số:**  
  Support = 0.0436 | Lift = 6.31
- **Hành động:**  
  Đảm bảo tồn kho đầy đủ, tránh hết hàng.

---

### 4️⃣ Tối ưu bố trí cửa hàng
- **Luật:**  
  `JUMBO BAG RED RETROSPOT → JUMBO STORAGE BAG SUKI`
- **Chỉ số:**  
  Lift = 5.75 | Confidence = 0.36
- **Hành động:**  
  Bày các sản phẩm này gần nhau để tăng xác suất mua kèm.

---

### 5️⃣ Chiến dịch marketing kết hợp sản phẩm
- **Luật:**  
  `LUNCH BAG RED RETROSPOT → LUNCH BAG BLACK SKULL`
- **Chỉ số:**  
  Lift = 6.46 | Confidence = 0.44
- **Hành động:**  
  Gửi voucher hoặc email gợi ý combo.

---

## 📈 Kết luận & Đề xuất

- **Cross-selling / Upselling:** dựa trên các luật Lift cao
- **Bố trí cửa hàng:** sắp xếp sản phẩm thường mua cùng nhau
- **Marketing cá nhân hóa:** dựa trên Confidence
- **Quản lý tồn kho:** ưu tiên các sản phẩm Support cao
- **Chiến dịch niche:** luật Lift cao nhưng Support thấp

---

## 📂 Cấu trúc Project

```text
shopping_cart_advanced_analysis/
├── data/
│   ├── raw/
│   │   └── online_retail.csv
│   └── processed/
│       ├── cleaned_uk_data.csv
│       ├── basket_bool.parquet
│       ├── rules_apriori_filtered.csv
│       └── rules_fpgrowth_filtered.csv
│
├── notebooks/
│   ├── preprocessing_and_eda.ipynb
│   ├── basket_preparation.ipynb
│   ├── apriori_modelling.ipynb
│   ├── fp_growth_modelling.ipynb
│   ├── weighted_rules.ipynb
│   ├── compare_apriori_fpgrowth.ipynb
│   └── runs/
│       ├── preprocessing_and_eda_run.ipynb
│       ├── basket_preparation_run.ipynb
│       ├── apriori_modelling_run.ipynb
│       ├── fp_growth_modelling_run.ipynb
│       ├── weighted_rules_run.ipynb
│       └── compare_apriori_fpgrowth_run.ipynb
│
├── src/
│   └── apriori_library.py
│
├── dashboard/
│   ├── app.py
│   └── requirements.txt
│
├── run_papermill.py
├── requirements.txt
└── README.md