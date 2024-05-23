import pygame

from Bullet import Bullets
from Direction import Direction
from EnemyHandler import EnemyHandler
from Ship import Player
from Sounds import Sounds
from Textures import Textures


class Events:

    @staticmethod
    def check_game_state(player: Player,
                         bullets: Bullets,
                         enemy_handler: EnemyHandler,
                         textures: Textures,
                         sounds: Sounds) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.move()
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.speed_x *= -1
            player.move()
            player.speed_x *= -1

        if keys[pygame.K_SPACE]:
            if player.can_shoot():
                bullet = player.shoot(textures["screen"].get_size()[1] // 32, enemy_handler.enemies, Direction.UP,
                                      textures["player_bullet"])

                bullets.append(bullet)

        return True
