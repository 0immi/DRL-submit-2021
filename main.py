import pygame, sys, time 
import torch
import collections
import random
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
# from IPython.display import clear_output
import matplotlib.pyplot as plt

from env import *

learning_rate = 0.0005
gamma = 0.98
buffer_size = 100000
batch_size = 32

class ReplayBuffer:
    def __init__(self):
        self.buffer = collections.deque(maxlen=buffer_size)

    def put(self,transition):
        self.buffer.append(transition)

    def sample(self, n):
        mini_bath = random.sample(self.buffer, n)
        state_list, action_list, reward_list, nextstate_list, done_list = [], [], [], [], []

        for transition in mini_bath:
            s, a, r, next_s, done = transition
            state_list.append(s)
            action_list.append([a])
            reward_list.append([r])
            nextstate_list.append(next_s)
            done_list.append([done])
            
        
        return torch.tensor(state_list, dtype=torch. float), torch.tensor(action_list), torch.tensor(reward_list), torch.tensor(nextstate_list, dtype = torch. float), torch.tensor(done_list)

    def size(self):
        return len(self.buffer)

class DQN(nn.Module):
    def __init__(self):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(8,128)
        self.fc2 = nn.Linear(128,128)
        self.fc3 = nn.Linear(128,5)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    
    def sample_action(self, obs, epsilon):
        out = self.forward(obs)
        coin = random.random()
        if coin < epsilon:
            return random.randint(0,1)
        else:
            return out.argmax().item()

def train(q, q_target, momory, optimizer,losses):
    for i in range(10):
        s,a,r,next_s, done = memory.sample(batch_size)

        q_out = q(s)
        q_a = q_out.gather(1,a)
        next_q_max = q_target(next_s).max (1)[0].unsqueeze(1)
        target = r + gamma*next_q_max*done
        loss = F.smooth_l1_loss(q_a.float(), target.float())
        
        losses.append(loss)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

def plot(reward):
    plt.plot(reward)
    plt.show()


env = env()
q = DQN()
q_target = DQN()
q_target.load_state_dict(q.state_dict())
memory = ReplayBuffer()

print_interval = 20
score = 0.0
scores  = []
losses = []
optimizer = optim.Adam(q.parameters(), lr=learning_rate)

time = 0
for n_epi in range(3000):
    epsilon = max(0.01, 0.08 - 0.01*(n_epi)/200)
    s = env.reset()
    done = False
    time = 0
    while not done:
        time += 1
        a = q.sample_action(torch.from_numpy(s). float (), epsilon)
        next_s, r, done = env.update(a)
        done_mask = 0.0 if done else 1.0
        memory.put((s,a,r,next_s,done_mask))
        s = next_s
        score += r

        if time == 300 or done:
            # plot(score)
            print(f"{n_epi} score is: {score/time}")
            scores.append(score/time)
            score = 0.0
            done = True

        if memory.size()>3000:
            train(q,q_target,memory,optimizer,losses)
        
        # if n_epi%print_interval==0 and n_epi !=0:
        #     q_target.load_state_dic(q_state_dic())
        #     print("n_episode : {}, score: {:.1f}, n_buffer : {}, eps : {:.1f}%".format (n_epi, score/print_interval, memory_size(), epsilon*100))
        #     score = 0.0


with open('reward.txt','w') as f:
    for item in scores:
        f.write("%d\n" %item)
with open('loss.txt','w') as f:
    for item in losses:
        f.write("%d\n" %item)    
