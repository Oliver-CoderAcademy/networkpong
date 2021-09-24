import socket
from exceptions import GameOver, SendBall
import time
import pygame
import os
import math

class Ball:
    def __init__(self, position, vector):
        self.position = position
        self.vector = vector
    
    def bounce_h(self):
        self.vector[1] = self.vector[1]*-1
        
    
    def bounce_v(self, faster=False, bias=0):
        self.vector[0] = self.vector[0]*-1
        self.vector[1]+=bias
        if faster:
            self.vector[1]+= int(math.copysign(1, self.vector[1]))

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
            ["|", "|"]+[" " for x in range(self.size-4)]+["|", "|"], 
            *[self.row(" ") for x in range(self.size//2-3)], 
            self.row("_")
        ]

    def move_ball(self):
        next_char = self.draw_paddle(self.table_matrix)[self.ball.next_position[0]][self.ball.next_position[1]]
        self.ball.move()
        if next_char == "=":
            self.ball.bounce_v(faster=True)
        if next_char == ">":
            self.ball.bounce_v(bias=1)
        if next_char == "<":
            self.ball.bounce_v(bias=-1)
        if next_char == "|":
            self.ball.bounce_h()
        if next_char == "~":
            print("sending")
            ballpos=self.ball.position
            ballvec=self.ball.vector
            self.ball=None
            raise SendBall(ballpos, ballvec)
            
        
    def draw_ball(self, matrix):
        if self.ball:
            matrix[self.ball.position[0]][self.ball.position[1]]="@"
            return matrix
        else:
            return matrix

    def draw_paddle(self, matrix):
        for x in range(self.paddle.position, self.paddle.position+4):
            if x-self.paddle.position==0:
                matrix[-1][x]="<"
            elif x-self.paddle.position==3:
                matrix[-1][x]=">"
            else:
                matrix[-1][x]="="
        return matrix

    def __repr__(self):
        return "\n".join(["".join(row) for row in self.draw_paddle(self.draw_ball(self.table_matrix))])

class Game:
    tablesize = 40
    
    def send_ball(self, position, vector):
        self.conn.sendall(bytes(f"{position[0]}, {position[1]}||{vector[0]}, {vector[1]}", "utf-8"))

    def __init__(self, issue_challenge=False):
        self.challenger = issue_challenge
        self.table = Table(self.tablesize)
        
        if not issue_challenge:
            self.table.ball = Ball((-2, self.tablesize//2), (-1, 0))
        
        if self.challenger:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind(("127.0.0.1", 65432))
            self.socket.listen()
            self.conn, self.addr = self.socket.accept()
            print("CONNECTED")
        else:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect(("127.0.0.1", 65432))
            print("CONNECTED")

        pygame.init()

        try:
            while True:
                if self.table.ball:
                    try:
                        self.table.move_ball() 
                        for x in range(5):
                            time.sleep(0.5)
                            os.system('cls' if os.name == 'nt' else 'clear')
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_LEFT:
                                        self.table.paddle.move(left=True)
                                    if event.key == pygame.K_RIGHT:
                                        self.table.paddle.move(left=False)
                            self.table.move_ball()
                            print(self.table)
                    except SendBall as s:
                        self.send_ball(s.position, s.vector)
                else:
                    position, vector = repr(self.conn.recv(1024)).strip("b'").split("||")
                    position = [int(position.split(", ")[0]), int(position.split(", ")[1])]
                    vector = [int(vector.split(", ")[0])*-1, int(vector.split(", ")[1])]
                    self.table.ball = Ball(position, vector)
                                    
        except GameOver as e:
            print(e.message)

        

       

        


