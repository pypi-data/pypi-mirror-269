from gymnasium import Env, spaces
import random
import math
import numpy as np
import pygame
import time

pygame.init()
class PocketTank(Env):
    def __init__(self):
        self.tank_1_positions_range = (50,150)
        self.tank_2_positions_range = (650,750)

        self.x1 = random.randint(*self.tank_1_positions_range)
        self.x2 = random.randint(*self.tank_2_positions_range)
        self.g = 12

        self.observation_space = spaces.MultiDiscrete([801,801,7])
        self.action_space = spaces.MultiDiscrete([100,90,3])

        self.action_cnt = 20
        self.remaining_actions = [self.action_cnt, self.action_cnt]

        self.v_wind = +8
        self.bullet_type = random.randint(0,6)

        self.w, self.h = 800, 500
        self._init_display()
        self.episodes = 0
        self.reward = 0
        self.tank_width = 56
        self.bullet_dist= 0

    def _get_boomerang_range(self, v, theta, g, air_factor = 7):
        theta = theta*math.pi/180
        if v*math.cos(theta)>0:
            dir = 1
        elif v*math.cos(theta)<0:
            dir = -1
        else:
            dir = 0
        range = (v**2)*math.sin(2*theta)/g - dir*0.5*air_factor*(v*math.cos(theta))**2/g**2
        return range
    
    def _get_range(self,action,tank,bullet_type):
        (v,angle,move) = action
        if(bullet_type==6):
            g = self.g
            range = self._get_boomerang_range(v,angle,g)
            return range
        if(bullet_type==5):
            v = min(50,v)
        rad_angle = math.radians(angle)
        vx = v * math.cos(rad_angle)
        vy = v * math.sin(rad_angle)
        if(tank==0):
            vx = vx + self.v_wind
        else : 
            vx = vx - self.v_wind
        
        range = ((2 * vy)/self.g) * vx
        return range

    def _get_bullet_position(self,action,tank,bullet_type):
        range = self._get_range(action,tank,bullet_type)
        x_bullet = 0 
        if(tank==0):
            x_bullet =  self.x1 + range
        else :
            x_bullet =  self.x2 - range
        return x_bullet

    def _get_diff(self,x_bullet,tank):
        diff = 0 
        if(tank==0):
            diff = abs(self.x2-x_bullet)
        else: 
            diff = abs(self.x1-x_bullet)
        return diff

    def _get_reward(self,diff, bullet_type):
        # reward = ....
        return 0

    def _check_for_end(self):
        if(self.remaining_actions == [0,0] or self.remaining_actions==[0,self.action_cnt]):
            return True
        else : 
            return False

    def _get_state(self):
        state = np.array([self.x1,self.x2,self.bullet_type])
        return state

    def _make_move(self,move,tank):
        if(tank==0):
            if(move==0):
                self.x1 = min(self.x1 + 25, 300)
            elif (move == 1):
                self.x1 = max(self.x1-25,0)
        else : 
            if(move==0):
                self.x2 = max(500,self.x2-25)
            elif(move == 1) : 
                self.x2 = min(798,self.x2+25)

    def step(self, action, tank=0):
        (v,angle,move) = action
        self._make_move(move,tank)
        bullet_type = self.bullet_type
        x_bullet = self._get_bullet_position(action,tank,bullet_type)
        diff = self._get_diff(x_bullet,tank)
        self.bullet_dist = diff
        reward = self._get_reward(diff,bullet_type)
        
        self.remaining_actions[tank]-=1
        done = self._check_for_end()
        self.bullet_type = random.randint(0,6)
        state = self._get_state()
        info = {"reward":reward}
        if(diff < self.tank_width/2):
            info["hit"]=True
        else : 
            info["hit"]=False
        truncated = False

        self.timesteps += 1
        self.reward += reward
        if self.episodes % 100 == 0 and self.timesteps < 10:
            self.bullet_buffer = self._get_bullet_pts(action)
            self.x_bullet = x_bullet
            self.turn = tank
            self.action = action
            self.render()
        
        return (state,reward,done,truncated,info)

    def reset(self,seed=None, values = None):
        self.x1 = random.randint(*self.tank_1_positions_range)
        self.x2 = random.randint(*self.tank_2_positions_range)
        self.remaining_actions = [self.action_cnt, self.action_cnt]
        state = self._get_state()
        info = {}

        self.episodes += 1
        self.timesteps = 0
        self.reward = 0
        self.bullet_dist = 0
        return (state,info)
    
    def _init_display(self):
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('TANKS')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 25) 
        self.FRAME_RATE = 60

    def _get_bullet_pts(self, action):
        pointsBuffer = [] 
        (v,angle,move) = action
        angle = math.radians(angle)

        vx = v * math.cos(angle)
        vy = v * math.sin(angle)
        vx = vx + self.v_wind
        for t in range(30):
            t = 0.5*t
            
            x_new = (self.x1)+vx*t
            y_new = 50+vy*t-0.5*self.g*t**2
            if y_new < 0:
                return pointsBuffer
            pointsBuffer.append((x_new, y_new))
        return pointsBuffer


    def render(self):
        self.display.fill((30, 30, 80))
        pygame.draw.rect(self.display, (50, 0, 0), (self.x1-28, self.h-100, 56, 50))
        pygame.draw.rect(self.display, (0, 0, 50), (self.x2-28, self.h-100, 56, 50))
        pygame.draw.rect(self.display, (140, 0, 0), (self.x1-28, self.h-100, 56, 50), 2)
        pygame.draw.rect(self.display, (0, 0, 140), (self.x2-28, self.h-100, 56, 50), 2)
        pygame.draw.rect(self.display, (20, 80, 0), pygame.Rect(0, self.h-50, self.w, 50))
        self.__draw_gui()

        pygame.draw.circle(self.display, (255, 255, 255), (self.x_bullet, 500-50), 5)
        pygame.draw.circle(self.display, (255, 255, 255), (self.x_bullet, 500-50), 8, 2)

        for i, point in enumerate(self.bullet_buffer):
            point = (point[0], 500-point[1])
            pygame.draw.circle(self.display, (255, 150, 150), (point[0], point[1]), 3)


        pygame.display.flip()
        self.clock.tick(self.FRAME_RATE)
        time.sleep(1)
        self.__handle_events()

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

    def __draw_gui(self):
        bullet_names = ['Standard Shell', 'Triple Threat', 'Long Shot', 'Blast Radius', 'Healing Halo', 'Heavy Impact', 'Boomerang Blast']
        bullet_colors = [(176, 196, 222), (147, 112, 219), (0, 139, 139), (255, 140, 0), (0, 250, 154), (178, 34, 34), (148, 0, 211)]
        pygame.draw.rect(self.display, (100, 130, 160), (5, self.h-5, self.w - 10, 200), 2)
        text = self.font.render(f'Episode: {self.episodes} ({self.timesteps}/20)', True, (255, 255, 255))
        self.display.blit(text, [300, 10])
        text = self.font.render(f'Reward: {str(self.reward)[:5]} Diff: {str(self.bullet_dist)}', True, (255, 255, 255))
        self.display.blit(text, [300, 60])
        text = self.font.render(bullet_names[self.bullet_type], True, bullet_colors[self.bullet_type])
        self.display.blit(text, [20, 50])
        text = self.font.render(f'Power: {self.action[0]}', True, (255, 0, 0))
        self.display.blit(text, [20, 80])
        text = self.font.render(f'Angle: {self.action[1]}', True, (180, 255, 250))
        self.display.blit(text, [20, 110])