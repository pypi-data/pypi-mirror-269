from sklearn.cluster import KMeans
import torch
import copy
import os
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_distances
from sklearn.metrics import silhouette_score
from tqdm import tqdm
class Kmean_base:
    def __init__(self,list_k,pruning_ratio):
        self.list_k = list_k
        self.pruning_ratio = pruning_ratio
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        
    def Kmean(self,weight,sort_index,k,output_channel):
        """
        Apply K-means clustering to perform filter pruning based on similarity in weight vectors.

        Args:
            weight: The weight tensor of the layer to be pruned.
            sort_index: The sorted indices of the weights.
            k: The number of clusters for K-means.
            output_channel: The number of output channels.

        Return:
            pruning_index_group: The indices of filters to be pruned.

        Logic:
            1. Determine the number of filters to be removed based on the output channel size.
            2. Reshape the weight tensor into a 2D matrix.
            3. Perform dimensionality reduction using PCA to reduce the dimensionality of weight vectors.
            4. Apply K-means clustering to the reduced weight vectors.
            5. Group the filters based on the K-means labels obtained.
            6. Prune filters from each group based on their importance and the required pruning amount.
                - Iterate over each group and calculate the pruning amount 
                  by multiplying the removal ratio with the total number of filters in the group.
                - Sort the indices of each group based on the specified sorted order, 
                  ensuring the original indices are preserved.
                - Select filters for pruning by popping from the end of the sorted indices until the 
                  desired pruning amount is reached.
            7. Return the indices of the pruned filters.

        
        """
        
        import time
        start = time.time()
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        num_filter = weight.shape[0]
        remove_filter = num_filter - output_channel
        if k == 1:
            return sort_index[output_channel:]
            
        
        m_weight_vector = weight.reshape(num_filter, -1)
        
        
        n_clusters = k

        kmeans = KMeans(n_clusters=n_clusters, random_state=0,n_init='auto').fit(m_weight_vector)
        
        # print("K:",n_clusters)
        labels = kmeans.labels_
        group = [[] for _ in range(n_clusters)]
        for idx in range(num_filter):
            group[labels[idx]].append(idx)
        lock_group_index = []
        copy_group = copy.deepcopy(group)
        for filter_index_group in copy_group:
            if len(filter_index_group) == 1:
                group.remove(filter_index_group)

        # The reminding item in group can be pruned by some crition
        pruning_index_group = []
        pruning_left_index_group = [[] for _ in range(len(group))]
        total_left_filter = sum(len(filter_index_group)
                                for filter_index_group in group)
        percentage_group = [int(
            100*(len(filter_index_group)/total_left_filter)) for filter_index_group in group]
        pruning_amount_group = [
            int(remove_filter*(percentage/100)) for percentage in percentage_group]
        sorted_idx_origin = copy.deepcopy(sort_index)
        for counter, filter_index_group in enumerate(group, 0):
            temp = copy.deepcopy(filter_index_group)
            temp.sort(key=lambda e: (list(sorted_idx_origin).index(e),e) if e in list(sorted_idx_origin)  else (len(list(sorted_idx_origin)),e))
            sorted_idx = torch.tensor(temp,device=device)
            filetr_index_group_temp = copy.deepcopy(list(sorted_idx))
            
            for sub_index in sorted_idx[len(sorted_idx)-pruning_amount_group[counter]:]:
                if len(filetr_index_group_temp) == 1:
                    continue
                pruning_index_group.append(filetr_index_group_temp.pop(filetr_index_group_temp.index(sub_index)))
            for left_index in filetr_index_group_temp:
                pruning_left_index_group[counter].append(left_index)
        # first one is the least important weight and the last one is the most important weight
        while (len(pruning_index_group) < remove_filter):
            pruning_amount = len(pruning_index_group)
            for left_index in pruning_left_index_group:
                if (len(left_index) <= 1):
                    continue
                if (len(pruning_index_group) >= remove_filter):
                    break
                pruning_index_group.append(left_index.pop(-1))
            if (pruning_amount >= len(pruning_index_group)):
                raise ValueError('infinity loop')
        return torch.tensor(pruning_index_group).to(device)
    
    def set_pruning_ratio(self,pruning_ratio):
        self.pruning_ratio = pruning_ratio

    def store_k_in_layer(self,layers):
        for layer in range(len(layers)//2):
            layers[layer*2].__dict__["k_value"] = self.list_k[layer]
            layers[layer*2].__dict__["bn"] = layers[(layer*2)+1].weight.data.clone()
