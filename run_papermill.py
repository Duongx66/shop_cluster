# Chạy Notebook Customer Clustering (Phân cụm khách hàng)
# Bạn cần tạo notebook 'notebooks/customer_segmentation.ipynb' để nhận các tham số này
pm.execute_notebook(
    "notebooks/customer_segmentation.ipynb",
    "notebooks/runs/customer_segmentation_run.ipynb",
    parameters=dict(
        RULES_PATH="data/processed/rules_fpgrowth_filtered.csv",
        CLEANED_DATA_PATH="data/processed/cleaned_uk_data.csv",
        
        # Thử nghiệm biến thể 1: Baseline (Chỉ dùng luật, dạng nhị phân)
        USE_RFM_V1=False,
        WEIGHTING_V1="binary",
        
        # Thử nghiệm biến thể 2: Nâng cao (Dùng luật có trọng số + RFM)
        USE_RFM_V2=True,
        WEIGHTING_V2="weighted",
        
        TOP_K_RULES=50,
        MAX_K_SEARCH=12,
        OUTPUT_CLUSTER_PATH="data/processed/customer_segments.csv"
    ),
    kernel_name="shopping_env",
)

print("--- TẤT CẢ PIPELINE ĐÃ HOÀN THÀNH ---")