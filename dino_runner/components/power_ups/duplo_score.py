from dino_runner.components.power_ups.power_up import PowerUp
from dino_runner.utils.constants import DEFAULT_TYPE, DUPLOSCORE


class DuploScore(PowerUp):
    def __init__(self):
        self.image = DUPLOSCORE
        self.type = DEFAULT_TYPE
        super().__init__(self.image,self.type)