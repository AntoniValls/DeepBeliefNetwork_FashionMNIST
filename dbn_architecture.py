# -*- coding: utf-8 -*-
"""
## Deep Belief Network

We create the DBN with the hyperparameters of our choice. We have checked several configurations and we have chosen the tunning with the best performance.
"""

dbn_fmnist = DBN(visible_units=28*28,               # dimensionality of the sensory data (28x28 grey images)
                hidden_units=[200, 400, 600, 800],  # size of hidden layers
                k=1,                                # reconstruction steps in Contrastive Divergence (we use CD-1)
                learning_rate=0.15,
                learning_rate_decay=False,
                initial_momentum=0.5,
                final_momentum=0.95,
                weight_decay=0.0001,
                xavier_init=False,
                increase_to_cd_k=False,
                use_gpu=torch.cuda.is_available())

"""We have decided to use the same number of epochs and batch size that we got during the Labs because of the similarity between the FashionMNIST dataset and the MNIST one."""

num_epochs = 50
batch_size = 125

dbn_fmnist.train_static(
    fmnist_tr.data,
    fmnist_tr.targets,
    num_epochs,
    batch_size
)

"""The best model we have found is composed of 4 hidden layers of size 200, 400, 600 and 800, it has a learning rate of 0.15 and uses CD-1.



"""
