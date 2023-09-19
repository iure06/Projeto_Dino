import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.utils.constants import (BG, DEFAULT_TYPE, FONT_STYLE, FPS,
                                         ICON, ICON_OVER, ICON_RESET, MUSIC,
                                         SCREEN_HEIGHT, SCREEN_WIDTH, TITLE)

HALF_SCREEN_HEIGHT = SCREEN_HEIGHT // 2
HALF_SCREEN_WIDTH = SCREEN_WIDTH // 2


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.score = 0
        self.death_count = 0
        self.best_Score = 0

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.score = 0
        self.game_speed = 20
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self)
        self.update_score()

    def update_score(self):
        self.score += 1
        if self.score % 500 == 0:
            self.game_speed += 2

        if self.best_Score < self.score:
            self.best_Score = self.score

        self.text_format(f"Score: {self.score}",1000,50, 22 , '#0000FF')
        self.text_format(f"Best Score: {self.best_Score}",800, 50,22,'#006400')
        self.text_format(f"Death: {self.death_count}", 70 , 50,22,'#FF0000')

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill('#FFFFFF')
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.update_score()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)

        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))

        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_power_up_time(self):
        if self.player.has_power_up:
            if not self.player.time:
                time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000,2)
                if time_to_show  >= 0:
                    self.text_format(
                        f"{self.player.type.capitalize()} enabled for {time_to_show} seconds",
                        HALF_SCREEN_WIDTH,
                        20,
                        22,
                        '#FF0000'
                    )
                else:
                    self.player.has_power_up = False
                    self.player.type = DEFAULT_TYPE

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.play_music(MUSIC)
                self.run()

    def show_menu(self):
        self.screen.fill((255,255,255))
        if self.death_count == 0:
            self.text_format('Press any key to start', HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT,30)
            self.screen.blit(ICON,(500,150))
        else:
            self.restart_screen_style()
            pygame.mixer.music.stop()

        pygame.display.update()
        self.handle_events_on_menu()        

    def restart_screen_style(self):
        self.screen.blit(ICON_OVER, (350, 100))
        self.text_format(f'Score: {self.best_Score}',HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT - 100,25,'#006400')
        self.text_format(f'Death: {self.death_count}',HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT - 70,25, '#FF0000')
        self.text_format('Press any key to restart', HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT,30)
        self.screen.blit(ICON_RESET, (HALF_SCREEN_WIDTH -35, 350))
        if self.death_count >= 20:
            self.text_format("You're really still here?, Congratulations on your dedication",HALF_SCREEN_WIDTH, 550,15, '#FF0000')
        
        if self.score <= 1000:
            self.text_format("Garoto, você esta pelo menos tentando?",HALF_SCREEN_WIDTH, 515,20, '#FF0000')
        elif self.score <= 3000:
            self.text_format("Esse é o seu melhor garoto?",HALF_SCREEN_WIDTH, 515,20, '#FF0000')
        elif self.score <= 5000:
            self.text_format("Até uma senhora faria melhor do que isso garoto",HALF_SCREEN_WIDTH, 515,20, '#FF0000')
        elif self.score <= 6000:
            self.text_format("Garoto um dia você me alcança",HALF_SCREEN_WIDTH, 515,20, '#FF0000')
        elif self.score >= 8000:
            self.text_format("Você esta quase lá garoto",HALF_SCREEN_WIDTH, 515,20, '#FF0000')
        elif self.score >= 12000:
            self.text_format("Meu jovem, você me superou!",HALF_SCREEN_WIDTH, 515,20, '#FF0000')


    def text_format(self,content,screen_x,screen_y,size = 22,color = "#000000"):
        font = pygame.font.Font(FONT_STYLE, size)
        text = font.render(content, True,color)
        text_rect = text.get_rect()
        text_rect.center = (screen_x,screen_y)
        self.screen.blit(text,text_rect)
    
    def play_music(self, music):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(music)
        pygame.mixer_music.play(-1)     