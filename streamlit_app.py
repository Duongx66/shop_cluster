import streamlit as st
import pandas as pd
import os

# Cấu hình trang
st.set_page_config(layout="wide", page_title="Shopping Cluster Analysis")
st.title("🚀 Customer Segmentation Dashboard")

# 1. Hàm Load dữ liệu
@st.cache_data
def load_data():
    path_profile = "data/processed/cluster_profiles.csv"
    path_rules = "data/processed/rules_fpgrowth_filtered.csv"
    
    if not os.path.exists(path_profile) or not os.path.exists(path_rules):
        st.error("⚠️ Không tìm thấy file dữ liệu tại data/processed/. Hãy kiểm tra lại thư mục!")
        st.stop()
        
    df_profiles = pd.read_csv(path_profile)
    df_rules = pd.read_csv(path_rules)
    return df_profiles, df_rules

df_profiles, df_rules = load_data()

# 2. Sidebar chọn Cụm (Sửa từ Rule_Cluster thành Cluster)
st.sidebar.header("Bộ lọc")
# Lấy danh sách cụm từ cột 'Cluster' trong file của bạn
cluster_list = df_profiles['Cluster'].unique().tolist()
selected_cluster = st.sidebar.selectbox("Chọn Cụm Khách Hàng:", cluster_list)

# 3. Hiển thị thông tin Cụm
st.header(f"📊 Phân tích đặc trưng Cụm: {selected_cluster}")

# Lấy dòng dữ liệu của cụm được chọn
cluster_data = df_profiles[df_profiles['Cluster'] == selected_cluster].iloc[0]

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📈 Chỉ số đặc trưng")
    # Kiểm tra nếu file có cột RFM thì hiển thị, nếu không thì báo bỏ qua
    if 'Monetary' in df_profiles.columns:
        st.metric("Monetary (Trung bình)", f"${cluster_data['Monetary']:,.2f}")
        st.metric("Frequency", f"{cluster_data['Frequency']:.1f}")
        st.metric("Recency", f"{cluster_data['Recency']:.0f} ngày")
    else:
        st.info("File này tập trung vào các đặc trưng quy luật (Rules).")

with col2:
    st.subheader("💡 Chiến lược gợi ý")
    # Logic đơn giản để phân loại
    if 'Monetary' in df_profiles.columns and cluster_data['Monetary'] > df_profiles['Monetary'].mean():
        st.success("**Nhóm Khách hàng VIP:** Ưu tiên chăm sóc đặc biệt và tặng quà tri ân.")
    else:
        st.info("**Nhóm Khách hàng Tiềm năng:** Gợi ý các sản phẩm đi kèm để tăng giá trị đơn hàng.")

st.divider()

# 4. Hiển thị các Quy luật (Rules) đặc trưng nhất của cụm này
st.subheader(f"🔗 Top 5 Quy luật mua sắm nổi bật của Cụm {selected_cluster}")

# Tìm tất cả các cột bắt đầu bằng chữ "Rule_" trong file của bạn
rule_cols = [c for c in df_profiles.columns if c.startswith("Rule_")]

if rule_cols:
    # Lấy giá trị của các cột Rule cho cụm này, sắp xếp giảm dần để tìm luật mạnh nhất
    cluster_rules_scores = df_profiles.loc[df_profiles['Cluster'] == selected_cluster, rule_cols].T
    cluster_rules_scores.columns = ['Score']
    top_rule_names = cluster_rules_scores.sort_values(by='Score', ascending=False).head(5).index

    display_rules = []
    for r_name in top_rule_names:
        try:
            # Tách số ID từ tên cột (Ví dụ: Rule_10 -> lấy số 10)
            rule_id = int(r_name.split('_')[1])
            if rule_id in df_rules.index:
                row = df_rules.iloc[rule_id]
                display_rules.append({
                    "Sản phẩm đã mua": row['antecedents'],
                    "Sản phẩm gợi ý": row['consequents'],
                    "Độ mạnh (Lift)": f"{row['lift']:.2f}",
                    "Mức độ liên quan cụm": f"{cluster_data[r_name]:.4f}"
                })
        except:
            continue
    
    if display_rules:
        st.table(pd.DataFrame(display_rules))
    else:
        st.warning("Không tìm thấy thông tin mô tả chi tiết cho các luật này.")
else:
    st.error("Không tìm thấy các cột 'Rule_X' trong file cluster_profiles.csv")