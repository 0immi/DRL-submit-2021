import pygame
import random
import numpy as np
from GenerateCar import *
from GenerateOtherCar import *

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
MIDDLE_x = 500
MIDDLE_y = 300
scale_x = 20
scale_y = 10
LANE = 3
SPEED = -3
MAXSPEED = -7
LANE_WIDHT = 4*scale_x
LANE1 = MIDDLE_x + LANE_WIDHT*(-1)
LANE2 = MIDDLE_x
LANE3 = MIDDLE_x + LANE_WIDHT*(1)

class env:
    def __init__ (self):
        #Initialize the game engine
        pygame.init()
        random.seed()

        #Set the height and width of the screen
        size = [SCREEN_WIDTH,SCREEN_HEIGHT]
        self.screen = pygame.display.set_mode(size)

        #Initialize the game clock
        self.clock = pygame.time.Clock()

        #Build background
        self.bg = pygame.image.load('/home/bluelagoon/Desktop/Project/bg.png')
        self.bg = pygame.transform.scale(self.bg,size)

        #Print text
        self.font = pygame.font.SysFont(None,30)
        self.text1 = self.font.render("Highway Environment",True,(0,0,0))

        #Position Autonomous car
        self.car = AutonomousCar()
        self.action = 0

        #For generating other cars
        self.objects = []
        self.events = []
        self.trigger_time = 0
        self.dis2other = 0
        self.accum_y = 0

        self.reward = 0


    def reset (self):
        self.clock = pygame.time.Clock()
        self.car = AutonomousCar()
        self.objects = []
        self.events = []
        self.trigger_time = 0
        self.accum_y = 0
        self.reward = 0
        self.action = 0

        return np.array([self.car.position[0],self.car.position[1],self.car.heading,self.car.speed, self.car.yaw, self.car.nearest_dis, self.car.nearest_dis2otherlane_right, self.car.nearest_dis2otherlane_left])

    def update(self,action):
        
        self.clock.tick(10)
        self.action = action

        # Generate other vehicles per trigger time
        self.trigger_time +=1 
        if self.trigger_time%50 == 0:
            # print("other car is generated")
            l = random.randint(1,LANE) #select lane randomly
            other_car = OtherCar(l)
            other_car.SelectBehavior(self.objects,self.car,-1)
            self.objects.append(other_car)
            self.trigger_time = 0
            
        
        # Update ego vehicle state
        self.car.update(self.action)
        dis2mid = MIDDLE_y - self.car.position[1]
        self.accum_y += dis2mid
        self.car.position[1] += dis2mid

        # Update other vehicle state
        if len(self.objects) >= 1:
            removeid = []
            for i, obj in enumerate(self.objects):

                self.objects[i].update()
                self.objects[i].position[1] = obj.position[1] + dis2mid
                self.objects[i].SelectBehavior(self.objects,self.car,i)

                if self.objects[i].position[1] > SCREEN_HEIGHT + 10: #remove the obj which goes outside of background
                    removeid.append(i)
                elif self.objects[i].position[1] < - 30:
                    removeid.append(i)


            if len(removeid) >= 1:
                # print(removeid)
                for id in removeid:
                    if id >= len(self.objects):
                        continue
                    self.objects.pop(id)

            self.car.dis2other(self.objects)

        #Calculate reward 
        if self.car.collided:
            reward_collision = -10000
        else:
            reward_collision = 0

        reward_dis2other = -5*(400-self.car.nearest_dis)
        reward_speed =  -5*(self.car.speed - MAXSPEED)
        reward_lanekeep = -self.car.dis2lane 
        reward_heading = -5*(self.car.heading**2)
        self.reward = reward_collision + reward_dis2other + reward_speed + reward_lanekeep + reward_heading 

        self.display()

        states = np.array([self.car.position[0], self.car.position[1], self.car.heading, self.car.speed, self.car.yaw, self.car.nearest_dis, self.car.nearest_dis2otherlane_right, self.car.nearest_dis2otherlane_left])

        return states, self.reward, self.car.done


         


    def display(self):
    
        # self.screen.fill([0,0,0])
        self.screen.blit(self.bg,self.bg.get_rect())
        self.screen.blit(self.text1,(5,5))
        pygame.display.set_caption("highway environment")

        self.screen.blit(self.car.car_rotated, [self.car.position[0], self.car.position[1]] )

        for id,obj in enumerate(self.objects):
            self.screen.blit(obj.car, obj.position)         

        
        self.text2 = self.font.render("Current Speed:    %d" %-self.car.speed,True,(0,0,0))
        self.screen.blit(self.text2,(5,35))

        self.text3 = self.font.render("Distance to nearest front object:     ",True,(0,0,0))
        if self.car.nearest_dis >= 1000 and self.car.nearest_dis2otherlane < 1000:
            self.text3 = self.font.render("Distance to nearest front object:    %d" %self.car.nearest_dis2otherlane,True,(0,0,0))
        elif self.car.nearest_dis < 1000 and self.car.nearest_dis2otherlane >= 1000:
            self.text3 = self.font.render("Distance to nearest front object:    %d" %self.car.nearest_dis,True,(0,0,0))
        else: 
            if  self.car.nearest_dis > self.car.nearest_dis2otherlane:
                self.text3 = self.font.render("Distance to nearest front object:    %d" %self.car.nearest_dis2otherlane,True,(0,0,0))
            elif self.car.nearest_dis < self.car.nearest_dis2otherlane:
                self.text3 = self.font.render("Distance to nearest front object:    %d" %self.car.nearest_dis,True,(0,0,0))
            else:
                self.text3 = self.font.render("Distance to nearest front object:     ",True,(0,0,0))

        self.screen.blit(self.text3,(5,55))
        
        self.text4 = self.font.render("Current Reward:    %d" %self.reward,True,(0,0,0))
        self.screen.blit(self.text4,(5,80))
        
        self.text4 = self.font.render("Current action:    %d" %self.action,True,(0,0,0))
        self.screen.blit(self.text4,(5,100))
        

        pygame.display.flip()
