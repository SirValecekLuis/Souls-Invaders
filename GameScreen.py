from sys import exit

import pygame

from TextHandler import TextHandler


class GameScreen:

    @staticmethod
    def intro_screen(screen: pygame.Surface):
        font = pygame.font.Font("font/OptimusPrinceps.ttf", 32)

        welcome_text, welcome_rect = TextHandler.get_centered_text("Welcome to invader souls",
                                                                   screen.get_height() // 3.2,
                                                                   font,
                                                                   screen)

        space_text, space_rect = TextHandler.get_centered_text("Press SPACE to start.",
                                                               screen.get_height() // 2.5,
                                                               font,
                                                               screen)

        movement_text, movement_rect = TextHandler.get_centered_text("Movement: WASD or arrows",
                                                                     screen.get_height() // 2,
                                                                     font,
                                                                     screen)

        shooting_text, shooting_rect = TextHandler.get_centered_text("Shooting: Spacebar",
                                                                     screen.get_height() // 1.8,
                                                                     font,
                                                                     screen)

        good_luck_text, good_luck_rect = TextHandler.get_centered_text("Good luck.",
                                                                       screen.get_height() // 1.4,
                                                                       font,
                                                                       screen)

        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                return

            screen.fill((0, 0, 0))
            screen.blit(welcome_text, welcome_rect)
            screen.blit(space_text, space_rect)
            screen.blit(movement_text, movement_rect)
            screen.blit(shooting_text, shooting_rect)
            screen.blit(good_luck_text, good_luck_rect)

            pygame.display.flip()

    @staticmethod
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

        pygame.time.delay(4500)
        pygame.quit()
        exit(0)

    @staticmethod
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
