"""The main file where all the functions are called and where the game loop is."""

import pygame.mixer
from pygame.constants import QUIT, KEYDOWN, KEYUP, FULLSCREEN, DOUBLEBUF  # pylint: disable=no-name-in-module

from buffs import Buffs
from bullet import Bullets
from effects import Effects
from enemy_handler import EnemyHandler
from events import Events
from game_screen import GameScreen
from ship import Player
from sounds import Sounds
from text_handler import TextHandler
from textures import Textures


# pylint: disable=fixme

# IMPORTANT FEATURES THAT SHOULD BE DONE FIRST
# TODO: game_screen and text_handler should be merged, it doesnt make sense now. + Write basic intro menu and ESC menu
#   ASAP and that will probably change the whole game_screen and text_handler file
# TODO: Write some game loop so player after dying will get back to menu and can play again without game shutting itself
# TODO: Add a menu when ESC key is pressed with stats like movement speed, damage etc.
# TODO: Replace intro screen with main menu

# FEATURES THAT SHOULD BE ADDED OR CONSIDERED
# TODO: Like sounds make textures loading dynamic based on dictionary access (not necessary for now)
#   And check in function add_texture() if the .convert_alpha() should be done after scaling or before
# TODO: Change that Bullet is not referencing Player and Player bullet, this cross reference is trash
# TODO: Change that texture for anything can be None and ensure it does not make any problem (draw just a casual rect)
# TODO: Add levels
# TODO: Add some special attacks and upgrades through the game as the player is leveling up
# TODO: Add text or particles when player has a buff
# TODO: FPS meter in right top corner that can be disabled or turned on in settings (clock.get_fps())
# TODO: Should merge all enums in one enum file?
# TODO: Standardize drawing, sometimes it is done by the instance itself,
#  sometimes by class that handles all instances...
# TODO: Rewrite waves and bosses
# TODO: Add some sort of currency (temporary, permanent for upgrades)
# TODO: Add some permanent upgrades for currency
# TODO: Create function update() that will handle ALL the calls like drawing, moving etc. or make some sub-funcs that
#   some will handle draw, some move etc. that's up to you in the future to decide
# TODO: Now the game is based on texture size, should be changed to rect size I guess?
# TODO: Do i need to call .set_volume for each sound effect in functions like destroying enemy or picking up a buff?
# TODO: Add a bloom in the future on shoots?

# OPTIMIZATION
# TODO: Optimize the game and try CProfiler to see what takes a lot of time,
#  try to reduce checking every frame to every second frame
# TODO: Optimize to check collision only with enemies on the same y axis as the enemy that is calculating the collision
# TODO: Maybe add some kind of parallelism or multithreading in the future?

def update_player(player: Player, screen: pygame.Surface) -> None:
    """Draws a player and checks if he is dead or not."""
    if player.hp <= 0:
        GameScreen.game_over_screen(screen)
    player.draw()


def main() -> None:
    """The main game loop."""
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.5)
    pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

    icon = pygame.image.load("./icon.png")
    pygame.display.set_icon(icon)

    flags = FULLSCREEN | DOUBLEBUF
    screen = pygame.display.set_mode((0, 0), flags, vsync=1, display=0)
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

        if not Events.check_game_state(player, bullets, enemy_handler, textures):   # pylint: disable=too-many-function-args
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
