import pygame
import bot  # subscriber modul

height = 600 # size of screen
width = 800

RED = (255, 0, 0)
BLUE = (0, 255, 0)
YELLOW = (45, 10, 15)
WHITE = (0, 0, 0)
FPS = 30


import time

from draw import *

class Robot():
    def init(self, x_start, y_start):   # задаем начальные координаты робота
        self.robot_height = 50  # размеры робота
        self.robot_width = self.robot_height
        self.angle = -90  # угол поворота
        self.speed = 0.005    # скорость робота
        self.rotation_speed = 1.8   # скорость поворота
        self.robotStarted = False   # робот запущен
        self.vector = pygame.math.Vector2(1, 0) # вектор направления движения
        self.robot = pygame.Surface((self.robot_height, self.robot_width), pygame.SRCALPHA) # создание поверхности робота
        self.robot.fill(YELLOW) # заливка цветом

        pygame.draw.line(self.robot, WHITE, [10, 0], [37, 0], 9)    # линия на роботе
        self.robot_rect = self.robot.get_rect(center =(x_start,y_start))    # получение координат прямоугольника

        self.previous_x_pos = 0
        self.previous_y_pos = 0

    def draw(self):
        self.rotated_robot = pygame.transform.rotozoom(self.robot, self.angle, 0.9)     # повернутая поверхность
        self.robot_rect = self.rotated_robot.get_rect(center=self.robot_rect.center)    # получение координат повернутого прямоугольника
        screen.blit(self.rotated_robot, self.robot_rect)     # отрисовка робота на экране по координатам прямоугольника

    def rotation(self, direction):
        if direction == 1:
            self.angle -= self.rotation_speed # поворот поверхности
            if self.angle <= -359: self.angle = 0
            self.vector.rotate_ip(+self.rotation_speed) # поврот вектора движения

        if direction == -1:
            self.angle += self.rotation_speed
            if self.angle >= 359: self.angle = 0
            self.vector.rotate_ip(-self.rotation_speed)

    def movement(self, move): 
        if move == 1:
            self.robot_rect.center += self.vector * 5.5
        if move == -1:
            self.robot_rect.center -= self.vector * 5.5

    def goTo(self, x_pos, y_pos, Rob_x, Rob_y): # на вход подаем координату места, куда ехать

        if self.robotStarted and self.robotAuto:  # если робот запущен
            dx = Rob_x - x_pos  # расчет расстояния до точки
            dy = Rob_y - y_pos
            dist = math.sqrt(dx * dx + dy * dy)  # расстояние до точки
            if dist != 0:
                vec_x = dx / dist  # косинус
                vec_y = dy / dist  # синус
            else:
                vec_x, vec_y = 1, 1

            vec2 = pygame.math.Vector2(-vec_x, -vec_y)  # вектор пайгейма
            vec2.normalize()  # нормализация вектора

            if math.fabs(self.vector.as_polar()[1] - vec2.as_polar()[1]) <= 1:
                self.movement(1)

            elif (vec2.as_polar()[1]<=0 and self.vector.as_polar()[1]>=0):
                if (math.fabs(self.vector.as_polar()[1]) + math.fabs(vec2.as_polar()[1]) >=180):
                    self.rotation(1)
                else:
                    self.rotation(-1)

            elif (vec2.as_polar()[1]>=0 and self.vector.as_polar()[1]<=0):
                if (math.fabs(self.vector.as_polar()[1]) + math.fabs(vec2.as_polar()[1]) >=180):
                    self.rotation(-1)
                else:
                    self.rotation(1)

            elif (self.vector.as_polar()[1]>0 and vec2.as_polar()[1]>0) :
                if math.fabs(self.vector.as_polar()[1]) > math.fabs(vec2.as_polar()[1]):
                    self.rotation(-1)
                else:
                    self.rotation(1)

            elif (self.vector.as_polar()[1]<0 and vec2.as_polar()[1]<0):
                if math.fabs(self.vector.as_polar()[1]) > math.fabs(vec2.as_polar()[1]):
                    self.rotation(1)
                else:
                    self.rotation(-1)

    def startRobot(self):
        self.robotStarted = True

    def stopRobot(self):
        self.robotStarted = False

    def auto(self):
        self.robotAuto = True

    def manual(self):
        self.robotAuto = False



def get_command(cmd):   # commands for movement
    if 'left' in cmd.strip():
        alpha_bot.rotation(1)

    if 'right' in cmd.strip():
        alpha_bot.rotation(-11)

    if 'forward' in cmd.strip():
        alpha_bot.movement(1)

    if 'stop' in cmd.strip():
        alpha_bot.stopRobot()


def main():

    bot.main()  # init modul bot 

    pygame.init()   

    screen = pygame.display.set_mode((width, height))   # screen 
    clock = pygame.time.Clock()
    screen.fill((20, 50, 60))

    done = False

    alpha_bot = Robot(0, 0)  # init robot
    alpha_bot.startRobot()  # start robot

    while not done:
        
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        #print(bot.cmd)

        get_command(bot.cmd)    # det cmd for robot from mqtt
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()