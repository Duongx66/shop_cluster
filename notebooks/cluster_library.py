import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns

class RuleBasedCustomerClusterer:
    def __init__(self, n_clusters=None):
        self.n_clusters = n_clusters
        self.rules = None
        self.feature_matrix = None
        self.model = None
        self.scaler = StandardScaler()

    def load_rules(self, rules_df, top_k=50, sort_by='lift'):
        """Lấy Top-K luật mạnh nhất để làm đặc trưng."""
        self.rules = rules_df.sort_values(by=sort_by, ascending=False).head(top_k)
        return self.rules

    def build_customer_item_matrix(self, df_transactions):
        """Tạo ma trận Khách hàng x Sản phẩm (Binary)."""
        return df_transactions.groupby(['customer_id', 'product_name']).size().unstack(fill_value=0) > 0

    def build_final_features(self, customer_item_matrix, use_rfm=False, rfm_df=None, weighting='binary'):
        """
        Trích xuất đặc trưng:
        - Binary: 1 nếu khách hàng có tất cả sản phẩm trong 'antecedents' của luật.
        - Weighted: Nhân với Lift/Confidence của luật đó.
        """
        features = pd.DataFrame(index=customer_item_matrix.index)
        
        for idx, rule in self.rules.iterrows():
            antecedents = list(rule['antecedents'])
            # Kiểm tra xem khách hàng có mua TOÀN BỘ các sản phẩm trong tiền đề không
            col_name = f"Rule_{idx}"
            has_antecedents = customer_item_matrix[antecedents].all(axis=1).astype(int)
            
            if weighting == 'lift':
                features[col_name] = has_antecedents * rule['lift']
            elif weighting == 'confidence':
                features[col_name] = has_antecedents * rule['confidence']
            else:
                features[col_name] = has_antecedents

        if use_rfm and rfm_df is not None:
            features = features.join(rfm_df, how='inner')
        
        # Chuẩn hóa dữ liệu (quan trọng cho K-Means)
        self.feature_matrix = pd.DataFrame(
            self.scaler.fit_transform(features),
            index=features.index,
            columns=features.columns
        )
        return self.feature_matrix

    def choose_k_by_silhouette(self, max_k=10):
        """Tìm K tối ưu bằng Silhouette Score."""
        scores = []
        K = range(2, max_k + 1)
        for k in K:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = km.fit_predict(self.feature_matrix)
            scores.append(silhouette_score(self.feature_matrix, labels))
        
        best_k = K[np.argmax(scores)]
        return best_k, scores

    def fit_kmeans(self, k):
        """Huấn luyện mô hình K-Means."""
        self.model = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = self.model.fit_predict(self.feature_matrix)
        return labels

    def project_2d(self, labels):
        """Giảm chiều PCA để trực quan hóa."""
        pca = PCA(n_components=2)
        components = pca.fit_transform(self.feature_matrix)
        
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=components[:, 0], y=components[:, 1], hue=labels, palette='viridis')
        plt.title(f'Customer Segmentation Visualization (K={len(np.unique(labels))})')
        plt.show()