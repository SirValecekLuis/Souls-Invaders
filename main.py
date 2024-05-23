import pygame.mixer
from pygame.locals import *

from Buffs import Buffs
from Bullet import Bullets
from Effects import Effects
from EnemyHandler import EnemyHandler
from Events import Events
from GameScreen import GameScreen
from Ship import Player
from Sounds import Sounds
from TextHandler import TextHandler
from Textures import Textures


# FEATURES TO ADD
# TODO: Add special attack for some key (like ctrl)
# TODO: Add maybe sound for ship getting hit
# TODO: Add text or particles when player has a buff
# TODO: Like sounds make textures loading dynamic based on dictionary access (not necessary for now)

# QUALITY OF CODE TODO: Add comments to each function in code

def update_player(player: Player,
                  screen: pygame.Surface) -> None:
    player.draw()
    if player.hp <= 0:
        GameScreen.game_over_screen(screen)


def main():
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.5)
    pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)

    flags = FULLSCREEN | DOUBLEBUF
    screen = pygame.display.set_mode((0, 0), flags, vsync=1)
    pygame.display.set_caption("Souls Invaders")
    clock = pygame.time.Clock()

    # Putting textures here to load them before the start of intro screen, the rest after load screen to diversify load
    textures = Textures(screen)
    # Start of the game
    GameScreen.intro_screen(screen)

    sounds = Sounds()
    # Player Ship
    player = Player(screen.get_size()[0] // 2 - 50,
                    screen.get_size()[1] - 100,
                    100,
                    100,
                    12,
                    0,
                    125,
                    10,
                    1,
                    textures["player"],
                    sounds,
                    textures["screen"])

    effects = Effects()
    bullets = Bullets()
    enemy_handler = EnemyHandler(sounds, textures, effects)
    text_handler = TextHandler()
    buffs = Buffs(player, textures, sounds, screen)
    pygame.time.wait(300)
    start_time = pygame.time.get_ticks()
    while True:
        clock.tick(60)
        screen.blit(textures["background"], (0, 0))

        # Handles all text on screen
        text_handler.show_ingame_text(player, start_time, screen)

        if not Events.check_game_state(player, bullets, enemy_handler, textures, sounds):
            break

        # Check everything and update
        update_player(player, screen)

        # check bullets
        bullets.check_bullets()
        bullets.draw_all_bullets()

        # Check enemies
        enemy_handler.check_enemies(player, bullets)
        enemy_handler.draw_all_enemies()

        # Check effects
        effects.update_all_effects()

        # check phase (spawning mobs)
        enemy_handler.check_phase(start_time)

        # generate and check buffs:
        buffs.spawn_buff()
        buffs.check_all_buffs()
        buffs.draw_all_buffs()

        # shows everything
        pygame.display.flip()

        # Clear the screen before the next frame
        screen.fill((0, 0, 0))

        # END OF THE GAME CYCLE
    pygame.quit()


if __name__ == "__main__":
    main()
