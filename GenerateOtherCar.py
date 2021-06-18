import pygame
import math
import numpy as np
import random

MIDDLE_x = 500
MIDDLE_y= 300
LANE_WIDHT = 80

scale_x = 20
scale_y = 10

scale_x = 20
scale_y = 10

class OtherCar:
    def __init__(self,lane):

        self.car = pygame.image.load('/home/bluelagoon/Desktop/Project/opponent_car.png')
        self.car = pygame.transform.scale(self.car, (30,50))

        pose_x = MIDDLE_x + LANE_WIDHT*(lane - 2)
        self.position = np.array([pose_x, -30])

        speed = random.randrange(4,9)
        self.speed = np.array([0, -speed])
        self.accelerate = np.array([0,0])
        self.lane = lane
        
    def SelectBehavior(self,others,ego,idx): # selct Slow or Keep behavior for target vehicle
        
        for i, obj in enumerate(others):

            if i == idx: #idx is index of target vehicle
                continue
                
            # if there is other car infront of target vehicle
            elif self.lane == obj.lane:
                if obj.position[1] < self.position[1]: 
                    dis = abs(obj.position[1] - self.position[1])
                    if dis <= 200:
                        self.speed[1] = obj.speed[1] + 3
                else:
                    self.speed[1] = self.speed[1]
            else:
                self.speed[1] = self.speed[1]

    def update(self):
        self.position = self.position + self.speed
