import random

from dino_runner.components.obstacles.obstacle import Obstacle


class Cactus(Obstacle):
    def __init__(self, image, size):
        self.type = random.randint(0,2)
        super().__init__(image,self.type)
        if size == 'small':
            self.rect.y = 325
        elif size == 'large':
            self.rect.y = 300