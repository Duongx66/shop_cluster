import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns

class RuleBasedCustomerClusterer:
    def __init__(self):
        self.rules = None
        self.feature_matrix = None
        self.model = None
        self.scaler = StandardScaler()

    def load_rules(self, rules_df, top_k=50, sort_by='lift', min_antecedent_len=1):
        """
        Lấy Top-K luật mạnh nhất. 
        Bổ sung: Lọc theo độ dài tiền đề (antecedent length) theo yêu cầu đề bài.
        """
        # Đảm bảo antecedents là tập hợp (frozenset)
        df = rules_df.copy()
        df['ant_len'] = df['antecedents'].apply(lambda x: len(x))
        
        # Lọc luật có độ dài tiền đề tối thiểu
        df = df[df['ant_len'] >= min_antecedent_len]
        
        # Sắp xếp và lấy Top-K
        self.rules = df.sort_values(by=sort_by, ascending=False).head(top_k)
        return self.rules

    def build_customer_item_matrix(self, df_transactions):
        """Tạo ma trận Khách hàng x Sản phẩm (Binary)."""
        # Lưu ý: 'customer_id' và 'product_name' phải khớp với data của bạn
        return df_transactions.groupby(['CustomerID', 'Description']).size().unstack(fill_value=0) > 0

    def build_final_features(self, customer_item_matrix, rfm_df=None, weighting='binary'):
        """
        Xây dựng 2 biến thể theo đề bài:
        1. Binary: Đặc trưng nhị phân (Baseline).
        2. Weighted: Trọng số (lift * confidence) + Ghép RFM (Nâng cao).
        """
        features = pd.DataFrame(index=customer_item_matrix.index)
        
        for idx, rule in self.rules.iterrows():
            antecedents = list(rule['antecedents'])
            col_name = f"Rule_{idx}"
            
            # Kiểm tra sản phẩm hiện có trong matrix không để tránh lỗi key
            valid_ants = [a for a in antecedents if a in customer_item_matrix.columns]
            if not valid_ants: continue
                
            has_antecedents = customer_item_matrix[valid_ants].all(axis=1).astype(int)
            
            if weighting == 'weighted':
                # Biến thể nâng cao: Trọng số lift * confidence
                features[col_name] = has_antecedents * (rule['lift'] * rule['confidence'])
            else:
                features[col_name] = has_antecedents

        # Ghép thêm RFM nếu là biến thể nâng cao
        if rfm_df is not None:
            # Đảm bảo rfm_df có index là CustomerID
            features = features.join(rfm_df, how='inner')
        
        # Lưu lại bản chưa scale để làm profiling sau này
        self.raw_features = features.copy()
        
        # Chuẩn hóa (Scale) toàn bộ matrix
        self.feature_matrix = pd.DataFrame(
            self.scaler.fit_transform(features),
            index=features.index,
            columns=features.columns
        )
        return self.feature_matrix

    def get_best_k(self, max_k=10):
        """Khảo sát K từ 2 đến max_k bằng Silhouette Score."""
        scores = []
        K_range = range(2, max_k + 1)
        for k in K_range:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = km.fit_predict(self.feature_matrix)
            scores.append(silhouette_score(self.feature_matrix, labels))
        
        best_k = K_range[np.argmax(scores)]
        return best_k, K_range, scores

    def fit_kmeans(self, k):
        self.model = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = self.model.fit_predict(self.feature_matrix)
        return labels

    def visualize_clusters(self, labels):
        """Giảm chiều PCA 2D và vẽ scatter plot."""
        pca = PCA(n_components=2)
        components = pca.fit_transform(self.feature_matrix)
        
        plt.figure(figsize=(10, 7))
        sns.scatterplot(x=components[:, 0], y=components[:, 1], hue=labels, palette='bright', alpha=0.7)
        plt.title(f'PCA Visualization - Customer Segments (K={len(np.unique(labels))})')
        plt.xlabel('PCA Component 1')
        plt.ylabel('PCA Component 2')
        plt.legend(title='Cluster')
        plt.show()

    def get_cluster_profiles(self, labels):
        """
        Phân tích đặc trưng từng cụm (Profiling).
        Trả về bảng thống kê trung bình RFM và các luật tiêu biểu.
        """
        df_profile = self.raw_features.copy()
        df_profile['Cluster'] = labels
        
        # Thống kê số lượng khách mỗi cụm
        cluster_size = df_profile.groupby('Cluster').size().reset_index(name='Size')
        
        # Thống kê trung bình các đặc trưng (RFM và Rule activation)
        profile_mean = df_profile.groupby('Cluster').mean()
        
        return cluster_size, profile_mean
    def compare_algorithms(self, k):
        """So sánh K-Means và Agglomerative Clustering (Yêu cầu mở rộng 1)"""
        results = []
        
        # 1. K-Means
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km_labels = km.fit_predict(self.feature_matrix)
        
        # 2. Agglomerative (Ward linkage)
        agg = AgglomerativeClustering(n_clusters=k)
        agg_labels = agg.fit_predict(self.feature_matrix)
        
        models = [('K-Means', km_labels), ('Agglomerative', agg_labels)]
        
        for name, labels in models:
            results.append({
                'Algorithm': name,
                'Silhouette': silhouette_score(self.feature_matrix, labels),
                'DBI': davies_bouldin_score(self.feature_matrix, labels),
                'CH_Score': calinski_harabasz_score(self.feature_matrix, labels)
            })
            
        return pd.DataFrame(results), km_labels, agg_labels