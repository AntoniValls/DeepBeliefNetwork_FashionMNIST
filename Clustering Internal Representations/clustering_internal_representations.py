# -*- coding: utf-8 -*-
"""
## Clustering internal representations

We can also investigate the characteristics of the acquired distributed representations. For instance, we can calculate the center of the representations learned for each category and determine their proximity to one another using a standard hierarchical clustering algorithm.

This implementation of the `DBN` contains internally several `RBM` objects. Therefore, we will need to compute the hidden representation using the weights of each `RBM`.
"""

def get_kth_layer_repr(input, k, device):
  flattened_input = input.view((input.shape[0], -1)).type(torch.FloatTensor).to(device)
  hidden_repr, __ = dbn_fmnist.rbm_layers[k].to_hidden(flattened_input)  # here we access the RBM object
  return hidden_repr

hidden_repr_1 = get_kth_layer_repr(fmnist_tr.data, 0, device)
hidden_repr_2 = get_kth_layer_repr(hidden_repr_1, 1, device)
hidden_repr_3 = get_kth_layer_repr(hidden_repr_2, 2, device)
hidden_repr_4 = get_kth_layer_repr(hidden_repr_3, 3, device)
print(hidden_repr_1.shape)
print(hidden_repr_2.shape)
print(hidden_repr_3.shape)
print(hidden_repr_4.shape)

def get_mask(label):  # we use this function to filter by class
  labels = fmnist_tr.targets.cpu().numpy()
  return labels == label

def get_label_to_mean_hidd_repr(hidden_repr):
  hidden_repr_np = hidden_repr.cpu().numpy()
  return {
    label: hidden_repr_np[get_mask(label)].mean(axis=0)  # here we filter by class and compute the mean
    for label in range(10)
  }

def get_hidden_reprs_matrix(hidden_repr):  # we use this to build the matrices
  label_to_mean_hidd_repr = get_label_to_mean_hidd_repr(hidden_repr)
  return np.concatenate(
    [np.expand_dims(label_to_mean_hidd_repr[label], axis=0)  # here we adjust the shape of centroids to do the concat
    for label in range(10)])

mean_hidd_repr_matrix_1 = get_hidden_reprs_matrix(hidden_repr_1)
mean_hidd_repr_matrix_2 = get_hidden_reprs_matrix(hidden_repr_2)
mean_hidd_repr_matrix_3 = get_hidden_reprs_matrix(hidden_repr_3)
mean_hidd_repr_matrix_4 = get_hidden_reprs_matrix(hidden_repr_4)

print(mean_hidd_repr_matrix_1.shape)
print(mean_hidd_repr_matrix_2.shape)
print(mean_hidd_repr_matrix_3.shape)
print(mean_hidd_repr_matrix_4.shape)

def plot_dendrogram(mean_repr_matrix, title=""):
  fig, ax = plt.subplots()
  linkage = cluster.hierarchy.linkage(mean_repr_matrix, method="complete")  # we run the clustering algorithm here
  dendrogram = cluster.hierarchy.dendrogram(linkage,
                                            labels = fmnist_tr.classes,
                                            leaf_rotation = 90,
                                            )
  ax.set_title(title)

plot_dendrogram(mean_hidd_repr_matrix_1, "First hidden layer")
plot_dendrogram(mean_hidd_repr_matrix_2, "Second hidden layer")
plot_dendrogram(mean_hidd_repr_matrix_3, "Third hidden layer")
plot_dendrogram(mean_hidd_repr_matrix_4, "Fourth hidden layer")

"""We can see in the dendograms that the body clothes have similar hidden representations among themselves (as we expected because of how the receptive fields were)."""
