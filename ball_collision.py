import random
import pygame
import math
import tkinter as tk
from tkinter import simpledialog


e = 1  # 반발력 계수를 나타냄

# tkinter 초기화
root = tk.Tk()
root.withdraw()

# 공의 갯수 입력받기
num_balls = simpledialog.askinteger("Input", "몇 개의 공을 확인하실건가요?", parent=root, minvalue=1, maxvalue=20)

# pygame 초기화
pygame.init()


# 창 크기 초기화
width, height = 300, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Colliding Balls')

class Ball:
    def __init__(self, x, y, m):
        self.pos = [x, y] #공의 초기 위치
        self.vel = [random.uniform(-0.05, 0.05), random.uniform(-0.05, 0.05)] #공의 초기 속도 랜덤으로 설정함
        self.acc = [0, 0] #공의 초기 가속도
        self.m = m #질량
        self.r = math.sqrt(m) * 10  # 질량에 기반하여 반지름 설정 -> 질량이 클수록 반지름이 더 커지도록 하기 위함
        #따라서 공의 크기 질량의 제곱근에 비례하도록 함
        self.isColliding = False #공이 충돌 중인지 나타냄
        self.collision_timer = 0  # 충돌 타이머 0으로 초기화
        self.collision_duration = 350  # 충돌 지속 시간 (프레임 수로 지정)
    
    #아래 설명에서의 두 번째 공은 두 공이 존재할 때의 다른 공을 가리키는 것임
    #self, other 중 other 공을 가리키는 것임

    def collisionDetection(self, other): #두 공 사이의 충돌을 감지함(self, other)
        displacement = [other.pos[0] - self.pos[0], other.pos[1] - self.pos[1]]
        #공의 중심 위치를 벡터로 나타낸 후 차를 구하여 중심을 잇는 벡터를 구함
        distance = math.sqrt(displacement[0] ** 2 + displacement[1] ** 2)
        #벡터의 x좌표와 y좌표를 제곱한 후 제곱근을 취하여 두 원 사이의 거리를 구함(피타고라스 사용)
        sumRadius = self.r + other.r #두 공의 반지름을 더한 값을 sumRadius에 저장함

        if distance <= sumRadius: 
            #distance(두 공 중심 사이 거리)가 sumRadius(두 공 반지름 합)보다 작다면 충돌함
            self.isColliding = True
            other.isColliding = True
            #충돌 중임을 나타내는 플래그(isColliding) True로 바꿈

            distanceCorrection = (sumRadius - distance) / 2.0
            #공이 충돌했을 때 두 공이 겹쳐지지 않도록 보정하기 위해 distanceCorrection을 
            #이용하여 공의 위치를 보정해줌
            #다시 말해 공이 겹쳤을 때, 공을 충돌 지점에서 반씩 이동시켜 겹침을 보정함
            #얼만큼 보정할 것인지를 계산하는 함수가 distanceCorrection
            correctionVector = [displacement[0] * (distanceCorrection / distance), displacement[1] * (distanceCorrection / distance)]
            #두 공이 겹쳤을 때, 얼마나 겹쳤는지에 따라 보정을 달리 해주기 위해 비율적으로 얼마나 이동해야
            #하는지를 설정함(실제로 얼마나 이동해야하는지를 나타냄)
            other.pos[0] += correctionVector[0]
            other.pos[1] += correctionVector[1]
            self.pos[0] -= correctionVector[0]
            self.pos[1] -= correctionVector[1]
            #앞서 설명한 correctionVector를 이용하여 충돌 지점을 보정함

            normal = [displacement[0] / distance, displacement[1] / distance]
            #충돌 지점을 향하는 벡터인 normal벡터를 구함
            #(단위벡터로 dispalment에 제곱근을 취한 distance로 나눔)

            u1 = self.vel[0] * normal[0] + self.vel[1] * normal[1]
            #self 공의 초기속도벡터와 충돌 방향 벡터의 내적을 계산함
            #self 공의 초기속도 벡터가 충돌 방향으로 얼마나 이루어져 있는지를 계산할 수 있음
            u2 = other.vel[0] * normal[0] + other.vel[1] * normal[1]
            #other 공의 초기속도벡터와 충돌 방향 벡터의 내적을 계산함
            #other 공의 초기속도 벡터가 충돌 방향으로 얼마나 이루어져 있는지를 계산할 수 있음
            normalVel1 = [normal[0] * u1, normal[1] * u1]
            #충돌 방향 벡터(normal)와 초기속도의 충돌 방향 성분(u1)을 곱함
            #이를 통해 첫 번째 공(self)의 충돌 방향으로의 속도를 나타내는 벡터를 얻을 수 있음
            normalVel2 = [normal[0] * u2, normal[1] * u2]
            #충돌 방향 벡터(normal)와 초기속도의 충돌 방향 성분(u2)을 곱함
            #이를 통해 두 번째 공(other)의 충돌 방향으로의 속도를 나타내는 벡터를 얻을 수 있음
            tangentVel1 = [self.vel[0] - normalVel1[0], self.vel[1] - normalVel1[1]]
            #첫 번째 공(self)의 충돌 방향과 수직인 방향으로의 속도를 나타냄
            #이는 첫 번째 공의 초기 x,y축 방향 속도 벡터에서 첫 번째 공의 충돌 방향으로의 속도 벡터를
            #뺌으로서 구할 수 있음
            tangentVel2 = [other.vel[0] - normalVel2[0], other.vel[1] - normalVel2[1]]
            #두 번째 공(other)의 충돌 방향과 수직인 방향으로의 속도를 나타냄
            #이는 두 번째 공의 초기 x,y축 방향 속도 벡터에서 두 번째 공의 충돌 방향으로의 속도 벡터를
            #뺌으로서 구할 수 있음
            m1, m2 = self.m, other.m
            #공의 질량을 각각 m1(첫 번째 공), m2(두 번째 공)에 저장함
            v1 = ((e + 1) * m2 * u2 + u1 * (m1 - e * m2)) / (m1 + m2)
            v2 = ((e + 1) * m1 * u1 + u2 * (m2 - e * m1)) / (m1 + m2)
            #(탄성)충돌에 대한 공식을 x축과 y축 각각 적용시킴
            #여기서 v1은 첫 번째, v2는 두 번째 물체의 속도를 나타냄
            #e는 반발력 계수로, 초기에 반발력 계수 1로 설정하였음
            #e=1: 완전 탄성 충돌, 운동량과 운동에너지 보존됨
            normalVel1 = [normal[0] * v1, normal[1] * v1]
            #첫 번째 공이 충돌 방향으로 이동하려는 속도를 나타냄
            #normal 벡터는 충돌하는 두 물체 사이의 충돌 방향을 가리킴
            #이 방향에 따른 속도(v1)을 곱하여 충돌 방향으로 이동하는 속도 성분 계산함
            normalVel2 = [normal[0] * v2, normal[1] * v2]
            #두 번째 공이 충돌 방향으로 이동하려는 속도를 나타냄
            #normal 벡터는 충돌하는 두 물체 사이의 충돌 방향을 가리킴
            #이 방향에 따른 속도(v2)을 곱하여 충돌 방향으로 이동하는 속도 성분 계산함
            
            #첫 번째 공(self)와 두 번째 공(other) 사이의 최종 속도 업데이트
            self.vel = [normalVel1[0] + tangentVel1[0], normalVel1[1] + tangentVel1[1]]
            other.vel = [normalVel2[0] + tangentVel2[0], normalVel2[1] + tangentVel2[1]]
            #normalVel1은 충돌 방향으로의 속도 성분이며, tangentVel1은 충돌 방향과 수직인 방향의 속도 성분
            #이 둘을 합하여 최종 속도를 업데이트함

    def applyForce(self, force): #공에 힘을 작용시킴
        f = [force[0] / self.m, force[1] / self.m]
        #힘 벡터(force)를 물체의 질량(self.m)으로 나누어서 가속도 계산함
        #뉴턴의 2번째 법칙 F=ma
        #따라서 a(가속도)=F(힘)/m(질량)
        self.acc[0] += f[0]
        #x축 방향으로의 가속도 계속 적용시킴
        self.acc[1] += f[1]
        #y축 방향으로의 가속도 계속 적용시킴

    #공이 화면 경계 밖으로 나가지 않도록 설정하기
    def edge(self):
        if self.pos[0] > width - self.r:
            #x축 위치가 화면 오른쪽의 경계를 벗어나면
            self.pos[0] = width - self.r
            #화면의 가로 길이에서 공의 반지름을 뺌
            self.vel[0] *= -1
            #x축 방향의 속도를 반대 방향으로 바꾸어줌
        elif self.pos[0] < self.r:
            #x축 위치가 화면 왼쪽의 경계를 벗어나면
            self.pos[0] = self.r
            #화면의 왼쪽 경계로 공을 이동시킴
            self.vel[0] *= -1
            #x축 방향의 속도를 반대 방향으로 바꾸어줌
        if self.pos[1] > height - self.r:
            #y축 위치가 화면 아래쪽의 경계를 벗어나면
            self.pos[1] = height - self.r
            #공의 y축 위치 화면의 아래 경계쪽으로 이동시킴
            self.vel[1] *= -1
            #y축 방향의 속도를 반대 방향으로 바꾸어줌
        elif self.pos[1] < self.r:
            #y축 위치가 화면 위쪽의 경계를 벗어나면
            self.pos[1] = self.r
            #공의 y축 위치 화면의 위쪽 경계쪽으로 이동시킴
            self.vel[1] *= -1
            #y축 방향의 속도를 반대 방향으로 바꾸어줌

    def update(self): #각 프레임마다 호출되어 공의 운동 상태 업데이트함
        self.vel[0] += self.acc[0]
        #현재 속도에 x축 가속도를 더하여 속도 업데이트함
        self.vel[1] += self.acc[1]
        #현재 속도에 y축 가속도를 더하여 속도 업데이트함
        self.pos[0] += self.vel[0]
        #현재 위치에 x축 속도를 더하여 속도 업데이트함
        self.pos[1] += self.vel[1]
        #현재 위치에 y축 속도를 더하여 속도 업데이트함
        self.acc = [0, 0]
        #다음 프레임에 새로운 가속도가 적용되기 전에 가속도 0으로 바꾸어줌

    def show(self):
        if self.isColliding: #공이 충돌 상태인지 확인함
            self.collision_timer = self.collision_duration  # 충돌 시 타이머 설정
        if self.collision_timer > 0: #충돌 타이머가 0보다 크다면
            pygame.draw.circle(screen, (255, 0, 0), (int(self.pos[0]), int(self.pos[1])), int(self.r))
            #(255, 0, 0)빨간색 원을 그리고
            self.collision_timer -= 1
            #충돌 타이머를 -1씩 감소시킴
            #self.collision_duration = 100으로 초기화 되어 있음
        else: #충돌이 감지되지 않았을 때 공을 그림
            pygame.draw.circle(screen, (200, 200, 200), (int(self.pos[0]), int(self.pos[1])), int(self.r))
            #(200, 200, 200) 회색

balls = []
for i in range(num_balls):
    balls.append(Ball(random.uniform(0, width), random.uniform(0, height), random.uniform(1, 2)))
#0과 width 사이 무작위 실수 x좌표, 0과 height 사이 무작위 실수 y좌표, 1과 2사이의 무작위 공의 질량을 지정함



running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #사용자가 창을 닫을 경우
            running = False

    #화면을 회식(220,220,220)으로 채움
    screen.fill((220, 220, 220))

    for i in range(len(balls)): #매 프레임마다 공 객체의 충돌 여부를 재설정함
        balls[i].isColliding = False #충돌 여부 false로 설정
        balls[i].edge() #화면 경계에 닿으면 튕겨나가도록 위치 조정함

    for i in range(len(balls)): #리스트의 모든 공 객체에 대해 충돌 감지
        for j in range(i + 1, len(balls)): #현재 공의 다음 index부터 공의 충돌을 감지함
            balls[i].collisionDetection(balls[j]) #i번째 공과 j번째 공의 충돌을 탐지하고 처리
        balls[i].update() #i번째 공의 위치와 속도 업데이트
        balls[i].show() #i번째 공을 그림

    pygame.display.update()

pygame.quit()