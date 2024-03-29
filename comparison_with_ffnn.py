"""
## Comparison with a feed-forward neural network

We will train a basic feed-forward neural network with relu activation functions and the same architecture as the DBN. This will allow us to compare a non-linear model that is trained end-to-end to solve a classification task with a simple linear classifier that uses representations of input data learned in an unsupervised way through the DBN.
"""

class Feedforward(torch.nn.Module):
  def __init__(self, first_hidden_layer_size, second_hidden_layer_size, third_hidden_layer_size, fourth_hidden_layer_size):
    super().__init__()
    self.first_hidden = torch.nn.Linear(784, first_hidden_layer_size)
    self.second_hidden = torch.nn.Linear(first_hidden_layer_size, second_hidden_layer_size)
    self.third_hidden = torch.nn.Linear(second_hidden_layer_size, third_hidden_layer_size)
    self.fourth_hidden = torch.nn.Linear(third_hidden_layer_size, fourth_hidden_layer_size)
    self.output = torch.nn.Linear(fourth_hidden_layer_size, 10)

  def forward(self, input):
    relu = torch.nn.ReLU()
    first_hidden_repr = relu(self.first_hidden(input))
    second_hidden_repr = relu(self.second_hidden(first_hidden_repr))
    third_hidden_repr = relu(self.third_hidden(second_hidden_repr))
    fourth_hidden_repr = relu(self.fourth_hidden(third_hidden_repr))
    output = self.output(fourth_hidden_repr)
    return output

ffnn = Feedforward(200, 400, 600, 800).to(device)

train_linear(ffnn, fmnist_tr.data.reshape((60000, 784)), "FFNN") # we need to flatten the images

predictions_ffnn = ffnn(fmnist_te.data.reshape((10000, 784)))

accffnn = compute_accuracy(predictions_ffnn, fmnist_te.targets)
print("The accuracy obtained using a Feed-Forward Neural Network is: {:.4f}".format(accffnn))

print("Accuracies obtained:")
print("{:<10} {:<10} {:<10} {:<10} {:<10}".format("Linear 1", "Linear 2", "Linear 3", "Linear 4", "FFNN"))
print("{:<10.4f} {:<10.4f} {:<10.4f} {:<10.4f} {:<10.4f}".format(acc1, acc2, acc3, acc4, accffnn))

"""As we can see the linear read out from the second hidden layer gives the best results."""
