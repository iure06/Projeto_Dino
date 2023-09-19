import random

from dino_runner.components.obstacles.obstacle import Obstacle


class Meteor(Obstacle):
    def __init__(self,image,size):
        self.type = 0
        self.image = image
        super().__init__(self.image, self.type)
        if size == 0:
            self.rect.y = 270
        else:
            self.rect.y = 315