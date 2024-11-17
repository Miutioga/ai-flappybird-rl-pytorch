import torch
from torch import nn
import torch.nn.functional as F

class DQN(nn.Module):

    def __init__(self, state_dim, action_dim, hidden_dim=256):
        super(DQN, self).__init__()

        self.fc1 = nn.Linear(state_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim*2)
        # self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        # self.fc3 = nn.Linear(hidden_dim, hidden_dim)
        # self.fc4 = nn.Linear(hidden_dim, hidden_dim)
        # self.fc5 = nn.Linear(hidden_dim, hidden_dim)
        # self.fc6 = nn.Linear(hidden_dim, hidden_dim)
        # self.fc7 = nn.Linear(hidden_dim, hidden_dim)
        # self.fc8 = nn.Linear(hidden_dim, hidden_dim)
        # self.fc9 = nn.Linear(hidden_dim, hidden_dim*2)
        self.output = nn.Linear(hidden_dim*2, action_dim)
        # self.output = nn.Linear(hidden_dim, action_dim)

    # x = state
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        # x = F.relu(self.fc3(x))
        # x = F.relu(self.fc4(x))
        # x = F.relu(self.fc5(x))
        # x = F.relu(self.fc6(x))
        # x = F.relu(self.fc7(x))
        # x = F.relu(self.fc8(x))
        # x = F.relu(self.fc9(x))
        return self.output(x)


if __name__ == '__main__':
    state_dim = 12
    action_dim = 2
    net = DQN(state_dim, action_dim)
    # state = torch.randn(10, state_dim)
    # output = net(state)
    # print(output)