from random import randint

import pygame
from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.meteor import Meteor
from dino_runner.utils.constants import (BIRD, LARGE_CACTUS, METEOR,
                                         SMALL_CACTUS)


class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        if len(self.obstacles) == 0:
            obstacleDraw = randint(0,3)
            
            if obstacleDraw == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS, 'small'))
            elif obstacleDraw == 1:
                self.obstacles.append(Cactus(LARGE_CACTUS, 'large'))
            elif obstacleDraw == 2:
                bird_y = randint(0, 1)
                self.obstacles.append(Bird(BIRD, bird_y))
            else:
                meteor_y = randint(0,1)
                self.obstacles.append(Meteor(METEOR,meteor_y))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.has_power_up:
                    pygame.time.delay(500)
                    game.playing = False
                    game.death_count += 1
                    break
                else:
                    if game.player.hammer:
                        self.obstacles.remove(obstacle)

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []