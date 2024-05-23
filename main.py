import pygame.mixer
from Ship import Ship
from GameScreen import GameScreen
from Bullet import Bullets
from Effects import Effects
from Textures import Textures
from Sounds import Sounds
from EnemyHandler import EnemyHandler
from Events import Events
from TextHandler import TextHandler


# TODO: Add some special effect or bonuses or anything
# TODO: Add a pause after boss fight like async 3s pause or something like that (maybe do check_enemies async? or add timer to dhat?)
# TODO: Add some time before enemy starts shooting fater spawning
# TODO: Add tips and hints to intro screen + explanation how to play
# TODO: Add special attack for some key (like ctrl)
# TODO: Add maybe sound for ship getting hit
# TODO: Winning music after completing the game
# TODO: Spawn some effect after spawning boss

# TODO: Fix shooting? / Change first boss, too easy


def update_player(player: Ship,
                  screen: pygame.Surface) -> None:
    player.draw()
    if player.hp <= 0:
        GameScreen.game_over_screen(screen)


def main():
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.7)
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Souls Invaders")
    clock = pygame.time.Clock()

    textures = Textures(screen)
    sounds = Sounds()
    effects = Effects()
    bullets = Bullets()
    enemy_handler = EnemyHandler()

    # Player Ship
    player = Ship(screen.get_size()[0] // 2 - 50,
                  screen.get_size()[1] - 100,
                  100,
                  100,
                  12,
                  0,
                  250,
                  1000,
                  1,
                  textures["player"],
                  textures["screen"])

    # Start of the game
    GameScreen.intro_screen(screen)
    pygame.time.wait(300)
    start_time = pygame.time.get_ticks()
    while True:
        clock.tick(60)
        screen.blit(textures["background"], (0, 0))

        if not Events.check_event(player, bullets, enemy_handler, textures, sounds):
            break

        # Handles all text on screen
        TextHandler.show_ingame_text(player, start_time, screen)

        enemy_handler.check_enemies(player, bullets, effects, textures, sounds)

        # Check everything and update
        update_player(player, screen)
        enemy_handler.update_all_enemies()
        effects.update_all_effects()
        bullets.update_all_bullets()

        # check phase (spawning mobs)
        enemy_handler.check_phase(start_time, textures, sounds)

        # shows everything
        pygame.display.flip()

        # Clear the screen before the next frame
        screen.fill((0, 0, 0))

        # END OF THE GAME CYCLE
    pygame.quit()


if __name__ == "__main__":
    main()
