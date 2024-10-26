from src.objects.bullet import Bullet


class BulletManager:
    """This class handles all projectiles that derive from class Bullet and will check collision and draws them."""

    def __init__(self):
        self.bullets = []

    def check_bullets(self) -> None:
        """Checks all the bullets and things that derive from Bullet class on the screen."""
        for i in range(len(self.bullets) - 1, -1, -1):
            bullet = self.bullets[i]
            if not bullet.check_bullet():
                self.bullets.pop(i)
                continue

    def draw_all_bullets(self):
        """Called every frame to draw all bullets on the screen and move them."""
        for bullet in self.bullets:
            bullet.draw()

    def append(self, bullet: Bullet):
        """Adds a Bullet class instance in the list to check on it next frame."""
        self.bullets.append(bullet)
