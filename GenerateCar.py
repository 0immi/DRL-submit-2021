import pygame
import math
import numpy as np

LENGTH = 2
MIDDLE_x = 500 
MIDDLE_y = 300

scale_x = 20
LANE_WIDHT = 4*scale_x
LANE1 = MIDDLE_x + LANE_WIDHT*(-1)
LANE2 = MIDDLE_x
LANE3 = MIDDLE_x + LANE_WIDHT*(1)


class AutonomousCar:
    def __init__(self):

        #car initial states
        self.position = np.array([MIDDLE_x, MIDDLE_y])
        self.speed = -5
        self.heading = 0
        self.yaw = 0
        self.accelerate = 0

        self.car = pygame.image.load('/home/bluelagoon/Desktop/Project/car.png')
        self.car = pygame.transform.scale(self.car, (30,50))
        self.car_rotated = pygame.transform.rotate(self.car, math.degrees(self.heading))

        self.lane = 2
        self.dis2lane = 0
        self.nearest_dis = 400
        self.nearest_dis2otherlane = 400
        self.nearest_dis2otherlane_left = 400
        self.nearest_dis2otherlane_right = 400

        self.collided = False
        self.done = False

    def update(self,action):

        if action == 0:
            a = 0
            yaw = 0
        elif action == 1:
            a = -1 
            yaw = 0
        elif action == 2:
            a = 1
            yaw = 0
        elif action == 3:
            a = 0
            yaw = -0.1
        else:
            a = 0
            yaw = 0.1

        self.position[0] += self.speed*math.sin(self.heading)
        self.position[1] += self.speed*math.cos(self.heading)
        self.heading += self.speed/LENGTH*math.tan(yaw)
        self.speed += a
        self.yaw = yaw

        if self.speed <= -7:
            self.speed = -7
        elif self.speed > 7:
            self.speed = 7


        self.done = False
        if self.position[0] >= LANE1-40 and self.position[0] < LANE1 + 40:
            self.lane = 1
            self.dis2lane = abs(LANE1-self.position[0])
        elif self.position[0] >= LANE2-40 and self.position[0] < LANE2 + 40:
            self.lane = 2
            self.dis2lane = abs(LANE2-self.position[0])
        elif self.position[0] >= LANE3-40 and self.position[0] < LANE3 + 40:
            self.lane = 3
            self.dis2lane = abs(LANE3-self.position[0])
        else:
            if self.position[0] < LANE1 - 40:
                self.position[0] = LANE1 - 41
                if self.dis2lane == 10000:
                    self.done = True
                else:
                    self.dis2lane = 10000
            
            else:
                self.position[0] = LANE3 + 41
                if self.dis2lane == 10000:
                    self.done = True
                else:
                    self.dis2lane = 10000

        self.car_rotated = pygame.transform.rotate(self.car, math.degrees(self.heading))

    def dis2other(self,objects):
        
        self.nearest_dis = 400
        self.nearest_dis2otherlane = 400
        for i, obj in enumerate(objects):
            if obj.lane == self.lane: 
                dis = math.sqrt((obj.position[0] - self.position[0])**2 + (obj.position[1] - self.position[1])**2)
                if obj.position[1] <= self.position[1]: #find nearest object in front of car
                    if dis < self.nearest_dis:
                        nearest_id = i
                        self.nearest_dis = dis
                elif dis <= 30:
                    if dis < self.nearest_dis:
                        nearest_id = i
                        self.nearest_dis = dis
                    
                    
            else: #find nearest object on the other lane
                dis2otherlane = math.sqrt((obj.position[0] - self.position[0])**2 + (obj.position[1] - self.position[1])**2) 
                if obj.lane == self.lane-1: #left lane
                    if dis2otherlane < self.nearest_dis2otherlane_left:
                        self.nearest_dis2otherlane_left = dis2otherlane
                elif obj.lane == self.lane+1: #right lane
                    if dis2otherlane < self.nearest_dis2otherlane_right:
                        self.nearest_dis2otherlane_right = dis2otherlane
                else:
                    self.nearest_dis2otherlane_right = 400
                    self.nearest_dis2otherlane_left = 400

        #For clipping
        self.nearest_dis2otherlane = 400
        if self.nearest_dis >= 400:
            self.nearest_dis = 400
        if self.nearest_dis <= 40:
            self.collided = True
            # print("collided")
        else:
            self.collided = False
        if self.nearest_dis2otherlane_left >= 400:
            self.nearest_dis2otherlane_left = 400
        if self.nearest_dis2otherlane_right >= 400:
            self.nearest_dis2otherlane_right = 400
        if self.nearest_dis2otherlane_left <= self.nearest_dis2otherlane_right:
            self.nearest_dis2otherlane = self.nearest_dis2otherlane_left
        else:
            self.nearest_dis2otherlane = self.nearest_dis2otherlane_right
