from GameClasses import *
import random


# TODO: add boom effect and sound effect
# TODO: after killing all mobs add more phases
# TODO: background?
# TODO: Add some special effect or bonuses or anything
# TODO: Add Timer text
# TODO: Add maybe some text that would tell you about the game and after pressing some key it would start the game?

def main():
    pygame.mixer.init()
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Souls Invaders")

    game_running = True
    clock = pygame.time.Clock()

    # Sound effects
    shot_fired_sound_effect = pygame.mixer.Sound("sounds/shot_sound.wav")
    shot_fired_sound_effect.set_volume(0.3)

    # Music
    pygame.mixer.music.load("sounds/background.mp3")
    # first_boss_music = pygame.mixer.Sound("sounds/first_boss.mp3")
    # second_boss_music = pygame.mixer.Sound("sounds/second_boss.mp3")

    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.7)

    # Textures
    player_texture = pygame.image.load("textures/player.png")
    player_texture = pygame.transform.scale(player_texture, (100, 100))

    enemy_texture = pygame.image.load("textures/enemy.png")
    enemy_texture = pygame.transform.scale(enemy_texture, (50, 50))

    player_bullet_texture = pygame.image.load("textures/player_bullet.png")
    player_bullet_texture = pygame.transform.scale(player_bullet_texture, (40, 40))

    enemy_bullet_texture = pygame.image.load("textures/enemy_bullet.png")
    enemy_bullet_texture = pygame.transform.scale(enemy_bullet_texture, (40, 40))

    # Texty
    font = pygame.font.Font(None, 32)

    # Ship
    player = Ship(screen.get_size()[0] // 2 - 50,
                  screen.get_size()[1] - 100,
                  100,
                  100,
                  12,
                  0,
                  100,
                  10,
                  player_texture,
                  screen)

    # Enemies
    enemies = []
    for i in range(10):
        enemy = Enemy(random.randrange(screen.get_width()),
                      i * enemy_texture.get_height(),
                      enemy_texture.get_width(),
                      enemy_texture.get_height(),
                      10,
                      0,
                      30,
                      10,
                      enemy_texture,
                      screen)
        enemies.append(enemy)

    while game_running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.move()
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.speed_x *= -1
            player.move()
            player.speed_x *= -1

        if keys[pygame.K_SPACE]:
            player.shoot(screen.get_size()[1] // 32, Direction.UP, player_bullet_texture, shot_fired_sound_effect)

        # Player
        player.draw()
        player.check_bullet(enemies)

        # Monstra
        for enemy in enemies:
            if not enemy.is_alive():
                enemies.remove(enemy)
                continue
            enemy.random_movement()
            enemy.draw()

        # Show text
        hp_text = font.render(f"HP:  {player.hp}", True, (255, 0, 0))
        screen.blit(hp_text, (10, screen.get_height() // 2))

        # shows everything
        pygame.display.flip()

        # Clear the screen before the next frame
        screen.fill((0, 0, 0))

        # END OF THE GAME CYCLE
    pygame.quit()


if __name__ == "__main__":
    main()
