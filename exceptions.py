class GameOver(Exception):
    pass

class SendBall(Exception):
    def __init__(self, position, vector):
        self.position=position
        self.vector=vector