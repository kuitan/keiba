import torch.nn as nn


class Ann(nn.Module):
    def __init__(self, input_dim, output_dim=2):
        super(Ann, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(128, 256),
            nn.BatchNorm1d(256, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(256, 128),
            nn.BatchNorm1d(128, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(128, output_dim),
            nn.Softmax(dim=0),
        )

    def forward(self, inputs):
        output = self.model(inputs)
        return output

