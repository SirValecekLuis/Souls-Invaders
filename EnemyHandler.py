import pygame
from Enemy import Enemy
import random
from Textures import Textures
from Sounds import Sounds
from Ship import Ship
from Bullet import Bullets
from Direction import Direction
from Effects import Effects
from GameScreen import GameScreen


class EnemyHandler:
    def __init__(self):
        self.phase = 1
        self.enemies = []

    def generate_enemy(self,
                       speed_x: float,
                       hp: float,
                       damage: float,
                       shooting_speed: float,
                       count: int,
                       boss: bool,
                       enemy_texture: pygame.Surface,
                       screen: pygame.Surface):
        if count > 50 or count < 0:
            raise Exception("Invalid amount of enemies to spawn")

        # For bosses
        if boss:
            enemy = Enemy(
                random.randrange(enemy_texture.get_width(), screen.get_width() - enemy_texture.get_width()),
                random.randrange(screen.get_height() // 10,
                                 screen.get_height() // 2 - enemy_texture.get_height()),
                enemy_texture.get_width(),
                enemy_texture.get_height(),
                speed_x,
                0,
                hp,
                damage,
                shooting_speed,
                enemy_texture,
                screen)
            self.enemies.append(enemy)
            return

        y_list = [i * enemy_texture.get_height() for i in
                  range(int(screen.get_height() // 2.5 // enemy_texture.get_height()))]
        i = 0
        collision = False
        while i < count:
            x = random.randrange(enemy_texture.get_width(), screen.get_width() - enemy_texture.get_width())
            y = random.choice(y_list)
            new_enemy = Enemy(x,
                              y,
                              enemy_texture.get_width(),
                              enemy_texture.get_height(),
                              speed_x,
                              0,
                              hp,
                              damage,
                              shooting_speed,
                              enemy_texture,
                              screen)

            for enemy in self.enemies:
                if new_enemy.rect.colliderect(enemy.rect):
                    collision = True
                    break

            if collision:
                collision = False
                continue

            self.enemies.append(new_enemy)
            i += 1

    def check_phase(self,
                    start_time: int,
                    textures: Textures,
                    sounds: Sounds) -> None:

        if len(self.enemies) != 0:
            return

        match self.phase:
            case 1:
                self.generate_enemy(10, 20, 3, 2, 15, False, textures["enemy"], textures["screen"])
                pygame.mixer.music.load("sounds/background.mp3")
                pygame.mixer.music.play()
            case 2:
                self.generate_enemy(15, 1000, 15, 0.45, 1, True, textures["boss_1"], textures["screen"])
                pygame.mixer.music.load("sounds/first_boss.mp3")
                pygame.mixer.music.play()
            case 3:
                self.generate_enemy(10, 25, 4, 1.5, 20, False, textures["enemy"], textures["screen"])
                pygame.mixer.music.load("sounds/background.mp3")
                pygame.mixer.music.play()
            case 4:
                self.generate_enemy(18, 2000, 30, 0.25, 1, True, textures["boss_2"], textures["screen"])
                pygame.mixer.music.load("sounds/second_boss.mp3")
                pygame.mixer.music.play()
            case _:
                if len(self.enemies) == 0:
                    GameScreen.game_completed_screen(start_time, textures["screen"])

        self.phase += 1

    def check_enemies(self,
                      player: Ship,
                      bullets: Bullets,
                      effects: Effects,
                      textures: Textures,
                      sounds: Sounds) -> None:
        i = 0
        while i < len(self.enemies):
            enemy = self.enemies[i]
            if not enemy.is_alive():
                effects.append(1, textures["boom_effect"], enemy.rect, textures["screen"])  # Explosion
                sounds["small_explosion"].play()  # Sound effect of explosion
                self.enemies.pop(i)
            else:
                enemy.random_movement(self.enemies)
                bullet = enemy.shoot(textures["screen"].get_size()[1] // 64, [player], Direction.DOWN,
                                     textures["enemy_bullet"], None)
                if bullet:
                    bullets.append(bullet)
                i += 1

    def update_all_enemies(self):
        for enemy in self.enemies:
            enemy.draw()
