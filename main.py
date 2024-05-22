import gif_pygame.transform
import pygame.mixer

from GameClasses import *


# TODO: Add some special effect or bonuses or anything
# TODO: Make a dictionary of textures and pass around (include screen)
# TODO: Add a pause after boss fight like async 3s pause or something like that
# TODO: Change music for different boss
# TODO: Add more shoots for bosses -> MORE info like
# TODO: Maybe do not bound shooting to existing bullet but rather a time passed (that could be used to set different timers for shooting for different enemies etc.)
# TODO: Add tips and hints to intro screen + explanation how to play
# TODO: Add special attack for some key (like ctrl)
# TODO: Add maybe sound for ship getting hit

def spawn_enemies(speed_x: float,
                  hp: int,
                  damage: int,
                  count: int,
                  boss: bool,
                  enemies: list,
                  enemy_texture: pygame.Surface,
                  screen: pygame.Surface) -> None:
    if count > 50 or count < 0:
        raise Exception("Invalid amount of enemies to spawn")

    # For bosses
    if boss:
        enemy = Enemy(random.randrange(enemy_texture.get_width(), screen.get_width() - enemy_texture.get_width()),
                      random.randrange(screen.get_height() // 4, screen.get_height() // 3),
                      enemy_texture.get_width(),
                      enemy_texture.get_height(),
                      speed_x,
                      0,
                      hp,
                      damage,
                      enemy_texture,
                      screen)
        enemies.append(enemy)
        return

    for i in range(count):
        enemy = Enemy(random.randrange(enemy_texture.get_width(), screen.get_width() - enemy_texture.get_width()),
                      i * enemy_texture.get_height(),
                      enemy_texture.get_width(),
                      enemy_texture.get_height(),
                      speed_x,
                      0,
                      hp,
                      damage,
                      enemy_texture,
                      screen)
        enemies.append(enemy)


def check_bullets(bullets: list) -> None:
    for bullet in bullets:
        if not bullet.check_bullet():
            bullets.remove(bullet)
            continue
        bullet.draw()


def check_player(player: Ship,
                 screen: pygame.Surface) -> None:
    player.draw()
    if player.hp <= 0:
        game_over_screen(screen)


def check_enemies(player: Ship,
                  enemies: list,
                  bullets: list,
                  effects: list,
                  common_enemy_destroyed: pygame.mixer.Sound,
                  boom_gif: gif_pygame.GIFPygame,
                  enemy_bullet_texture: pygame.Surface,
                  screen: pygame.Surface) -> None:
    for enemy in enemies:
        if not enemy.is_alive():
            enemies.remove(enemy)
            effects.append(Effect(1, boom_gif, enemy.rect, screen))  # Explosion
            common_enemy_destroyed.play()  # Sound effect of explosion
            continue
        enemy.random_movement()
        bullet = enemy.shoot(screen.get_size()[1] // 64, [player], Direction.DOWN, enemy_bullet_texture, None)
        if bullet:
            bullets.append(bullet)
        enemy.draw()


def check_effects(effects: list) -> None:
    for effect in effects:
        if not effect.update():
            effects.remove(effect)
            continue


def check_phase(enemies: list,
                phase: int,
                enemy_texture: pygame.Surface,
                first_boss_texture: pygame.Surface,
                last_boss_texture: pygame.Surface,
                screen: pygame.Surface) -> int:
    if len(enemies) != 0:
        return phase

    match phase:
        case 1:
            spawn_enemies(10, 30, 10, 10, False, enemies, enemy_texture, screen)
        case 2:
            spawn_enemies(5, 200, 30, 1, True, enemies, first_boss_texture, screen)
        case 3:
            spawn_enemies(10, 30, 10, 10, False, enemies, enemy_texture, screen)
        case 4:
            spawn_enemies(5, 500, 30, 1, True, enemies, last_boss_texture, screen)
        case _:
            game_completed_screen(screen)

    return phase + 1


def check_event(player: Ship,
                bullets: list,
                enemies: list,
                player_bullet_texture: pygame.Surface,
                shot_fired_sound_effect: pygame.mixer.Sound,
                screen: pygame.Surface) -> bool:
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
        bullet = player.shoot(screen.get_size()[1] // 32, enemies, Direction.UP, player_bullet_texture,
                              shot_fired_sound_effect)
        if bullet:
            bullets.append(bullet)

    return True


def intro_screen(screen: pygame.Surface):
    font = pygame.font.Font("font/OptimusPrinceps.ttf", 32)

    welcome_text = font.render(f"Welcome to Souls Invader.\n", True, (129, 0, 1))
    welcome_text.blit(welcome_text, (10, screen.get_height() // 2))
    welcome_rect = welcome_text.get_rect()
    welcome_rect.center = (screen.get_width() // 2, screen.get_height() // 3)

    space_text = font.render(f"Press SPACE to start.", True, (129, 0, 1))
    space_text.blit(space_text, (10, screen.get_height() // 2))
    space_rect = space_text.get_rect()
    space_rect.center = (screen.get_width() // 2, screen.get_height() // 2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return

        screen.fill((0, 0, 0))
        screen.blit(welcome_text, welcome_rect)
        screen.blit(space_text, space_rect)

        pygame.display.flip()


def game_over_screen(screen: pygame.Surface):
    font = pygame.font.Font("font/OptimusPrinceps.ttf", 72)
    game_over_text = font.render("YOU DIED", True, (89, 0, 1))
    text_rect = game_over_text.get_rect()
    text_rect.center = (screen.get_width() // 2, screen.get_height() // 2)

    # Music
    pygame.mixer.music.load("sounds/game_over.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(1)

    screen.fill((0, 0, 0))
    screen.blit(game_over_text, text_rect)

    pygame.display.flip()

    pygame.time.delay(7_300)
    pygame.quit()
    exit(0)


def game_completed_screen(screen: pygame.Surface):
    print("Hra skončila.")


def show_text(player: Ship,
              start_time: float,
              screen: pygame.Surface):
    font = pygame.font.Font("font/OptimusPrinceps.ttf", 24)

    hours, remainder = divmod(pygame.time.get_ticks() - start_time, 3_600_000)
    minutes, seconds = divmod(remainder, 60_000)
    seconds //= 1000

    time_text = font.render(f"Time: {hours}h {minutes}m {seconds}s", True, (255, 0, 0))
    screen.blit(time_text, (10, screen.get_height() // 2))

    hp_text = font.render(f"HP:  {player.hp}", True, (255, 0, 0))
    screen.blit(hp_text, (10, screen.get_height() // 2 + time_text.get_height()))


def main():
    pygame.mixer.init()
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Souls Invaders")

    clock = pygame.time.Clock()

    # Sound effects
    shot_fired_sound_effect = pygame.mixer.Sound("sounds/shot_sound.wav")
    shot_fired_sound_effect.set_volume(0.3)

    common_enemy_destroyed = pygame.mixer.Sound("sounds/small_explosion.wav")
    common_enemy_destroyed.set_volume(0.5)

    # Music
    pygame.mixer.music.load("sounds/background.mp3")
    # first_boss_music = pygame.mixer.Sound("sounds/first_boss.mp3")
    # second_boss_music = pygame.mixer.Sound("sounds/second_boss.mp3")

    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.7)

    # Textures
    background_texture = pygame.image.load("textures/background.png")
    background_texture = pygame.transform.scale(background_texture, (screen.get_width(), screen.get_height()))

    player_texture = pygame.image.load("textures/player.png")
    player_texture = pygame.transform.scale(player_texture, (100, 100))

    enemy_texture = pygame.image.load("textures/enemy.png")
    enemy_texture = pygame.transform.scale(enemy_texture, (50, 50))

    first_boss_texture = pygame.image.load("textures/boss_1.png")
    first_boss_texture = pygame.transform.scale(first_boss_texture, (150, 150))

    last_boss_texture = pygame.image.load("textures/boss_2.png")
    last_boss_texture = pygame.transform.scale(last_boss_texture, (250, 250))

    player_bullet_texture = pygame.image.load("textures/player_bullet.png")
    player_bullet_texture = pygame.transform.scale(player_bullet_texture, (40, 40))

    enemy_bullet_texture = pygame.image.load("textures/enemy_bullet.png")
    enemy_bullet_texture = pygame.transform.scale(enemy_bullet_texture, (40, 40))

    boom_gif = gif_pygame.load("textures/boom_effect.gif")

    effects = []

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
    phase = 1
    enemies = []

    # bullet
    bullets = []

    # intro
    intro_screen(screen)
    pygame.time.wait(300)

    start_time = pygame.time.get_ticks()
    #
    #
    #
    # GAME LOOP
    #
    #
    #
    while True:
        clock.tick(60)
        screen.blit(background_texture, (0, 0))

        if not check_event(player, bullets, enemies, player_bullet_texture, shot_fired_sound_effect, screen):
            break

        # Handles all text on screen
        show_text(player, start_time, screen)

        # Check what is going on
        check_player(player, screen)
        check_enemies(player, enemies, bullets, effects, common_enemy_destroyed, boom_gif, enemy_bullet_texture, screen)
        check_effects(effects)
        check_bullets(bullets)

        # check phase
        phase = check_phase(enemies, phase, enemy_texture, first_boss_texture, last_boss_texture, screen)

        # shows everything
        pygame.display.flip()

        # Clear the screen before the next frame
        screen.fill((0, 0, 0))

        # END OF THE GAME CYCLE
    pygame.quit()


if __name__ == "__main__":
    main()
