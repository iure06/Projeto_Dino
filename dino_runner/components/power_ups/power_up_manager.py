import random

import pygame
from dino_runner.components.power_ups.duplo_score import DuploScore
from dino_runner.components.power_ups.hammer import Hammer
from dino_runner.components.power_ups.luck_box import LuckBox
from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.time import Time
from dino_runner.utils.constants import HAMMER_TYPE, SHIELD_TYPE


class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appers = random.randint(500,900)

    def generate_power_up(self, score):
        if len(self.power_ups) == 0 and score >= self.when_appers:
            self.power = random.randint(0,4)
            self.when_appers += random.randint(500,900)
            if self.power == 0:
                self.power_ups.append(Shield())
            elif self.power == 1:
                self.power_ups.append(Hammer())
            elif self.power == 2:
                self.power_ups.append(Time())
            elif self.power == 3:
                self.duplo_score = random.randint(1,4)
                if self.duplo_score == 1:
                    self.power_ups.append(DuploScore())
            else:
                self.power_ups.append(LuckBox())

    def update(self,game):
        # score, game_speed, player
        self.generate_power_up(game.score)
        for power_up in self.power_ups:
            power_up.update(game.game_speed, self.power_ups)
            if game.player.dino_rect.colliderect(power_up.rect):
                power_up.start_time = pygame.time.get_ticks()
                if self.power == 0:
                    game.player.shield = True
                    game.player.hammer = False
                    game.player.time = False
                    self.player_config(game.player, power_up)
                elif self.power == 1: 
                    game.player.hammer = True
                    game.player.shield = False
                    game.player.time = False
                    self.player_config(game.player, power_up)
                elif self.power == 2:
                    game.player.hammer = False
                    game.player.shield = False
                    fast_or_slow = random.randint(0,1)
                    if fast_or_slow == 0:
                        game.game_speed += 5
                    else:
                        game.game_speed -= 10
                elif self.power == 3:
                    if self.duplo_score == 1:
                        game.score *= 2
                else:
                    self.luck_box_random = random.randint(0,2)
                    if self.luck_box_random == 0:
                        game.player.shield = True
                        game.player.hammer = False
                        game.player.slow = False
                        self.player_config(game.player, power_up)
                        game.player.type = SHIELD_TYPE
                    elif self.luck_box_random == 1: 
                        game.player.hammer = True
                        game.player.shield = False
                        game.player.slow = False
                        self.player_config(game.player, power_up)
                        game.player.type = HAMMER_TYPE
                    elif self.luck_box_random == 2:
                        game.player.hammer = False
                        game.player.shield = False
                        fast_or_slow = random.randint(0,1)
                        if fast_or_slow == 0:
                            game.game_speed += 10
                        else:
                            game.game_speed -= 10

                self.power_ups.remove(power_up)

    def player_config(self,player,power_up):
        player.has_power_up = True
        player.type = power_up.type
        player.power_up_time = power_up.start_time + (power_up.duration * 1000)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_ups(self):
        self.power_ups = []
        self.when_appers = random.randint(500,900)