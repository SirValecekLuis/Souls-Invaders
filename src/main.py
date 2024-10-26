"""The main file where all the functions are called and where the game loop is."""
import pygame

from src.managers.buff_manager import BuffManager
from src.managers.bullet_manager import BulletManager
from src.managers.effect_manager import EffectManager
from src.managers.enemy_manager import EnemyManager
from src.managers.event_manager import EventManager
from src.managers.sound_manager import SoundManager
from src.managers.service_manager import ServiceManager
from src.managers.time_manager import TimeManager
from src.managers.text_manager import TextManager
from src.managers.texture_manager import TextureManager
from src.managers.screen_manager import ScreenManager
from src.objects.ship import Player
from src.menu.main_menu import MainMenu


# pylint: disable=fixme

# IMPORTANT FEATURES THAT SHOULD BE DONE FIRST
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

def update_player(player: Player) -> None:
    """Draws a player and checks if he is dead or not."""
    if player.hp <= 0:
        # TODO: end game
        ...
    player.draw()


def main() -> None:
    """The main game loop."""

    screen = ScreenManager()
    ServiceManager.register(ScreenManager, screen)

    sounds = SoundManager()
    ServiceManager.register(SoundManager, sounds)

    # Load them before game starts
    textures = TextureManager()
    ServiceManager.register(TextureManager, textures)

    time_manager = TimeManager()
    ServiceManager.register(TimeManager, time_manager)

    # Start of the game
    menu = MainMenu()
    menu.start()

    # Player Ship
    player = Player(screen.get_width() // 2 - 50,
                    screen.get_height() - 100,
                    100,
                    100,
                    12,
                    0,
                    125,
                    10,
                    1,
                    textures["player"])

    effects = EffectManager()
    ServiceManager.register(EffectManager, effects)

    bullets = BulletManager()
    ServiceManager.register(BulletManager, bullets)

    enemy_manager = EnemyManager()
    ServiceManager.register(EnemyManager, enemy_manager)

    text_handler = TextManager()
    ServiceManager.register(TextManager, text_handler)

    buffs = BuffManager(player)
    ServiceManager.register(BuffManager, buffs)

    events = EventManager(player)
    ServiceManager.register(EventManager, events)

    while True:
        screen.blit(textures["background"], (0, 0))

        # Handles all text on screen
        text_handler.render_text(player)

        if not events.check_game_state():
            break

        # Check everything and update
        update_player(player)

        # check bullets
        bullets.check_bullets()
        bullets.draw_all_bullets()

        # Check enemies
        enemy_manager.check_enemies(player)
        enemy_manager.draw_all_enemies()

        # Check effects
        effects.update_all_effects()

        # check phase (spawning mobs)
        enemy_manager.check_phase()

        # generate and check buffs:
        buffs.spawn_buff()
        buffs.check_all_buffs()
        buffs.draw_all_buffs()

        # shows everything
        pygame.display.flip()

        # update time
        time_manager.update()

        # Clear the screen before the next frame
        screen.get_screen().fill((0, 0, 0))

        # END OF THE GAME CYCLE
    pygame.quit()


if __name__ == "__main__":
    main()
