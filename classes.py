import socket
from exceptions import GameOver
import time
import pygame

class Ball:
    def __init__(self, position, vector):
        self.position = position
        self.vector = vector
    
    def bounce_h(self, faster=False):
        self.vector[1] = self.vector[1]*-1
    
    def bounce_v(self):
        self.vector[0] = self.vector[0]*-1

    @property
    def next_position(self):
        return self.position[0]+self.vector[0], self.position[1]+self.vector[1]
    
    def move(self):
        self.position = self.next_position

class Paddle:
    def __init__(self, tablesize):
        self.position = tablesize//2-1
        self.tablesize = tablesize

    def move(self, left=True):
        if left and self.position>1:
            self.position-=1
        elif self.position<self.tablesize-5:
            self.position+=1

class Table:
    def __init__(self, size):
        self.size = size
        self.paddle = Paddle(size)
        self.ball = None

    def row(self, char):
        return ["|"]+[char for x in range(self.size-2)]+["|"]

    @property
    def table_matrix(self):
        return [
            self.row("~"), 
            *[self.row(" ") for x in range(self.size//2-2)], 
            self.row("_")
        ]

    def move_ball(self):
        pass

    def draw_ball(self, matrix):
        if self.ball:
            matrix[self.ball.position[0]][self.ball.position[1]]="@"
            return matrix
        else:
            return matrix

    def draw_paddle(self, matrix):
        for x in range(self.paddle.position, self.paddle.position+4):
            if x-self.paddle.position==0 or x-self.paddle.position==3:
                matrix[-1][x]="-"
            else:
                matrix[-1][x]="="
        return matrix

    def __repr__(self):
        pass

class Game:
    tablesize = 40
    
    def send_ball():
        pass

    def __init__(self, opponent, issue_challenge=False):
        self.challender = issue_challenge
        self.table = Table(self.tablesize)
        if issue_challenge:
            self.table.ball = Ball((-2, self.tablesize//2), (-1, 0))
        self.opponent = opponent

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((opponent, 65432))

        pygame.init()

        try:
            while True:
                if self.table.ball:
                    self.table.move_ball()
                    for x in range(5):
                        time.sleep(0.04)
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_LEFT:
                                    print("Hey, you pressed the key, '0'!")
                                if event.key == pygame.K_RIGHT:
                                    print("Doing whatever")

        except GameOver:
            pass
