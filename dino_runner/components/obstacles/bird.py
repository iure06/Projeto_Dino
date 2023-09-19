from dino_runner.components.obstacles.obstacle import Obstacle


class Bird(Obstacle):
    def __init__(self, image, bird_y):
        self.type = 0
        super().__init__(image,self.type)
        if bird_y == 0:
            self.rect.y = 270
        else:
            self.rect.y = 315
        self.step_index = 0

    def draw(self, screen):
        if self.step_index >= 9:
            self.step_index = 0
        screen.blit(self.image[self.step_index//5],self.rect)
        self.step_index += 1