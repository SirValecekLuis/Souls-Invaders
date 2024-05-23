import gif_pygame.transform
import pygame.mixer

from GameClasses import *


# TODO: Add some special effect or bonuses or anything
# TODO: Make a dictionary of textures and pass around (include screen)
# TODO: Add a pause after boss fight like async 3s pause or something like that
# TODO: Add tips and hints to intro screen + explanation how to play
# TODO: Add special attack for some key (like ctrl)
# TODO: Add maybe sound for ship getting hit
# TODO: Winning music after completing the game

# TODO: Fix shooting? / Change first boss, too easy

def spawn_enemies(speed_x: float,
                  hp: float,
                  damage: float,
                  shooting_speed: float,
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
        enemies.append(enemy)
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

        for enemy in enemies:
            if new_enemy.rect.colliderect(enemy.rect):
                collision = True
                break

        if collision:
            collision = False
            continue

        enemies.append(new_enemy)
        i += 1


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
                  textures: Textures,
                  sounds: Sounds) -> None:
    i = 0
    while i < len(enemies):
        enemy = enemies[i]
        enemy.draw()
        if not enemy.is_alive():
            effects.append(Effect(1, textures["boom_effect"], enemy.rect, textures["screen"]))  # Explosion
            sounds["small_explosion"].play()  # Sound effect of explosion
            enemies.pop(i)
        else:
            enemy.random_movement(enemies)
            bullet = enemy.shoot(textures["screen"].get_size()[1] // 64, [player], Direction.DOWN,
                                 textures["enemy_bullet"], None)
            if bullet:
                bullets.append(bullet)
            i += 1


def check_effects(effects: list) -> None:
    for effect in effects:
        if not effect.update():
            effects.remove(effect)
            continue


def check_phase(enemies: list,
                phase: int,
                start_time: int,
                textures: Textures,
                sounds: Sounds) -> int:
    if len(enemies) != 0:
        return phase

    match phase:
        case 1:
            spawn_enemies(10, 20, 3, 2, 20, False, enemies, textures["enemy"], textures["screen"])
            pygame.mixer.music.load("sounds/background.mp3")
            pygame.mixer.music.play()
        case 2:
            spawn_enemies(15, 1000, 15, 0.3, 1, True, enemies, textures["boss_1"], textures["screen"])
            pygame.mixer.music.load("sounds/first_boss.mp3")
            pygame.mixer.music.play()
        case 3:
            spawn_enemies(10, 25, 4, 1.5, 25, False, enemies, textures["enemy"], textures["screen"])
            pygame.mixer.music.load("sounds/background.mp3")
            pygame.mixer.music.play()
        case 4:
            spawn_enemies(18, 2000, 30, 0.25, 1, True, enemies, textures["boss_2"], textures["screen"])
            pygame.mixer.music.load("sounds/second_boss.mp3")
            pygame.mixer.music.play()
        case _:
            if len(enemies) == 0:
                game_completed_screen(start_time, textures["screen"])

    return phase + 1


def check_event(player: Ship,
                bullets: list,
                enemies: list,
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
        bullet = player.shoot(textures["screen"].get_size()[1] // 32, enemies, Direction.UP, textures["player_bullet"],
                              sounds["shot_sound"])
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


def game_completed_screen(start_time, screen: pygame.Surface):
    font = pygame.font.Font("font/OptimusPrinceps.ttf", 72)

    game_completed_text = font.render("CONGRATULATIONS!", True, (89, 0, 1))
    game_completed_rect = game_completed_text.get_rect()
    game_completed_rect.center = (screen.get_width() // 2, screen.get_height() // 3)

    hours, remainder = divmod(pygame.time.get_ticks() - start_time, 3_600_000)
    minutes, seconds = divmod(remainder, 60_000)
    seconds //= 1000

    time_text = font.render(f"Time passed: {hours}h {minutes}m {seconds}s", True,
                            (89, 0, 1))
    time_rect = time_text.get_rect()
    time_rect.center = (screen.get_width() // 2, screen.get_height() // 2)

    screen.fill((0, 0, 0))
    screen.blit(game_completed_text, game_completed_rect)
    screen.blit(time_text, time_rect)

    pygame.display.flip()

    pygame.time.delay(7_300)
    pygame.quit()
    exit(0)


def show_ingame_text(player: Ship,
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
    pygame.mixer.music.set_volume(0.7)
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Souls Invaders")
    clock = pygame.time.Clock()

    textures = Textures(screen)
    sounds = Sounds()

    # Enemies
    phase = 1
    enemies = []

    # bullet
    bullets = []

    # Textures
    effects = []

    # Player Ship
    player = Ship(screen.get_size()[0] // 2 - 50,
                  screen.get_size()[1] - 100,
                  100,
                  100,
                  12,
                  0,
                  250,
                  10,
                  1,
                  textures["player"],
                  textures["screen"])

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
        screen.blit(textures["background"], (0, 0))

        if not check_event(player, bullets, enemies, textures, sounds):
            break

        # Handles all text on screen
        show_ingame_text(player, start_time, screen)

        # Check what is going on
        check_player(player, screen)
        check_enemies(player, enemies, bullets, effects, textures, sounds)
        check_effects(effects)
        check_bullets(bullets)

        # check phase
        phase = check_phase(enemies, phase, start_time, textures, sounds)

        # shows everything
        pygame.display.flip()

        # Clear the screen before the next frame
        screen.fill((0, 0, 0))

        # END OF THE GAME CYCLE
    pygame.quit()


if __name__ == "__main__":
    main()
