# -*- coding: utf-8 -*-
"""
## Robustness to noise

Now, we will add noise to the input images to evaluate the robustness of the representations learned by the DBN and the feed-forward network to perturbations in the sensory signal. This will enable us to create a psychometric curve that describes the decline in classification accuracy as a function of the noise level, similar to what is observed in psychophysical experiments.
"""

def inject_noise(fmnist_data, noise_level):

  # injecting noise function
  noised_mnist_data = (fmnist_data + noise_level * torch.randn(fmnist_data.shape).to(device))

  return noised_mnist_data

"""Let's see what a noisy image looks like:"""

noise_level = 0.3
fmnist_test_with_noise = inject_noise(fmnist_te.data, noise_level)
idx = 3

fig, axes = plt.subplots(1,2, figsize = (10,15))
axes[0].imshow(fmnist_test_with_noise[idx].reshape(28, 28).to("cpu"), cmap="gray")
axes[0].set_title("With noise")
axes[0].axis('off')
axes[1].imshow(fmnist_te.data[idx].to("cpu"), cmap="gray")
axes[1].set_title("Without noise")
axes[1].axis('off')

plt.show()

"""Our next step is to calculate the hidden representations for the noisy images using the DBN. We will then use the read-out classifiers that we trained on the representations without noise to classify the noisy stimuli."""

def get_accuracy_values_at_noise_level(noise_level):

  # first, let's create noisy test images
  fmnist_test_with_noise = inject_noise(fmnist_te.data, noise_level)

  # compute the DBN representations in each hidden layer
  hidden_repr_1_noisy = get_kth_layer_repr(fmnist_test_with_noise, 0, device)  # here we compute the DBN representations
  hidden_repr_2_noisy = get_kth_layer_repr(hidden_repr_1_noisy, 1, device)
  hidden_repr_3_noisy = get_kth_layer_repr(hidden_repr_2_noisy, 2, device)
  hidden_repr_4_noisy = get_kth_layer_repr(hidden_repr_3_noisy, 3, device)

  # make predictions with the previously-trained read-out classifiers
  predictions_first_hidden_noisy = linear1(hidden_repr_1_noisy)
  predictions_second_hidden_noisy = linear2(hidden_repr_2_noisy)
  predictions_third_hidden_noisy = linear3(hidden_repr_3_noisy)
  predictions_fourth_hidden_noisy = linear4(hidden_repr_4_noisy)

  # get the accuracies of each linear read out in the test set
  accuracy_first_hidden = compute_accuracy(predictions_first_hidden_noisy, fmnist_te.targets)
  accuracy_second_hidden = compute_accuracy(predictions_second_hidden_noisy, fmnist_te.targets)
  accuracy_third_hidden = compute_accuracy(predictions_third_hidden_noisy, fmnist_te.targets)
  accuracy_fourth_hidden = compute_accuracy(predictions_fourth_hidden_noisy, fmnist_te.targets)

  # also for the FFNN
  predictions_ffnn = ffnn(fmnist_test_with_noise.reshape((10000, 784)))
  accuracy_ffnn = compute_accuracy(predictions_ffnn, fmnist_te.targets)

  return accuracy_first_hidden, accuracy_second_hidden, accuracy_third_hidden, accuracy_fourth_hidden, accuracy_ffnn

acc = get_accuracy_values_at_noise_level(0.3);
print("Accuracy of H1 read-out: %.3f" % acc[0])
print("Accuracy of H2 read-out: %.3f" % acc[1])
print("Accuracy of H3 read-out: %.3f" % acc[2])
print("Accuracy of H4 read-out: %.3f" % acc[3])
print("Accuracy of FF network : %.3f" % acc[4])

"""The linear read out from the fourth hidden layer is the one that gives us better results when using noisy data.

We will generate psychometric curves for the DBN and feed-forward network at various levels of internal representations.
"""

def plot_noise_robustness_curves(noise_levels):
  accuracy_values_first_hidden = []
  accuracy_values_second_hidden = []
  accuracy_values_third_hidden = []
  accuracy_values_fourth_hidden = []
  accuracy_values_ffnn = []

  for noise_level in noise_levels:
    acc = get_accuracy_values_at_noise_level(noise_level)
    accuracy_values_first_hidden.append(acc[0])
    accuracy_values_second_hidden.append(acc[1])
    accuracy_values_third_hidden.append(acc[2])
    accuracy_values_fourth_hidden.append(acc[3])
    accuracy_values_ffnn.append(acc[4])

  fig, ax = plt.subplots()
  ax.plot(range(len(noise_levels)), accuracy_values_first_hidden)
  ax.plot(range(len(noise_levels)), accuracy_values_second_hidden)
  ax.plot(range(len(noise_levels)), accuracy_values_third_hidden)
  ax.plot(range(len(noise_levels)), accuracy_values_fourth_hidden)
  ax.plot(range(len(noise_levels)), accuracy_values_ffnn)

  ax.set_title("Robustness to noise")
  ax.set_xlabel("Noise level (%)")
  ax.set_ylabel("Accuracy")
  plt.xticks(range(len(noise_levels)), [int(l*100) for l in noise_levels])
  plt.legend(["First hidden", "Second hidden", "Third hidden", "Fourth hidden", "FFNN"])

noise_levels = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]
plot_noise_robustness_curves(noise_levels)

"""The results indicate that linear read outs on deeper layers of DBN maintain better performance against noise than shallower layers. This suggests that deeper layers of DBN are more robust to perturbations in the sensory signal."""
