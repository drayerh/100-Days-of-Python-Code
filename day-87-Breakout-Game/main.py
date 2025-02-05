import pygame
import random
import math
from os import path

# Constants
WIDTH, HEIGHT = 800, 600  # Screen dimensions
FPS = 60  # Frames per second
COLORS = {
    "background": (30, 30, 30),
    "paddle": (200, 200, 200),
    "ball": (255, 75, 75),
    "brick1": (50, 200, 50),
    "brick2": (200, 50, 50),
    "brick3": (50, 50, 200),
    "powerup": (255, 255, 100)
}

class Paddle:
    """Class representing the paddle in the game."""

    def __init__(self):
        """Initialize the paddle with default attributes."""
        self.width = 120
        self.height = 20
        self.speed = 10
        self.rect = pygame.Rect(WIDTH // 2 - self.width // 2, HEIGHT - 50, self.width, self.height)
        self.normal_width = self.width

    def move(self, direction):
        """
        Move the paddle left or right.

        Args:
            direction (str): Direction to move the paddle ('left' or 'right').
        """
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= self.speed
        if direction == "right" and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def reset(self):
        """Reset the paddle to its initial position and width."""
        self.width = self.normal_width
        self.rect = pygame.Rect(WIDTH // 2 - self.width // 2, HEIGHT - 50, self.width, self.height)

class Ball:
    """Class representing the ball in the game."""

    def __init__(self):
        """Initialize the ball with default attributes."""
        self.radius = 10
        self.reset()
        self.speed = 6
        self.max_speed = 8

    def reset(self):
        """Reset the ball to its initial position and speed."""
        self.speed = 6
        self.rect = pygame.Rect(WIDTH // 2 - self.radius, HEIGHT // 2 - self.radius,
                                self.radius * 2, self.radius * 2)
        angle = math.radians(random.choice([30, 45, 135, 150]))
        self.dx = math.cos(angle) * self.speed
        self.dy = -math.sin(angle) * self.speed

    def move(self):
        """Move the ball and handle wall collisions."""
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Wall collisions
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.dx *= -1
        if self.rect.top <= 0:
            self.dy *= -1

class Brick:
    """Class representing a brick in the game."""

    def __init__(self, x, y, tier=1):
        """
        Initialize the brick with its position and tier.

        Args:
            x (int): The x-coordinate of the brick.
            y (int): The y-coordinate of the brick.
            tier (int): The tier of the brick (default is 1).
        """
        self.width = 75
        self.height = 30
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.tier = tier
        self.hits_remaining = tier
        self.colors = [COLORS["brick1"], COLORS["brick2"], COLORS["brick3"]]

    @property
    def color(self):
        """Return the color of the brick based on its tier."""
        return self.colors[self.tier - 1]

class PowerUp:
    """Class representing a power-up in the game."""

    def __init__(self, x, y):
        """
        Initialize the power-up with its position.

        Args:
            x (int): The x-coordinate of the power-up.
            y (int): The y-coordinate of the power-up.
        """
        self.size = 20
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.speed = 3
        self.type = random.choice(["expand", "slow", "multiball"])

    def move(self):
        """Move the power-up downwards."""
        self.rect.y += self.speed

class Game:
    """Class representing the game."""

    def __init__(self):
        """Initialize the game, load assets, and reset the game state."""
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Modern Breakout")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.load_assets()
        self.reset_game()

    def load_assets(self):
        """Load game assets such as sounds."""
        self.snd_dir = path.join(path.dirname(__file__), 'sounds')
        self.hit_sound = pygame.mixer.Sound(path.join(self.snd_dir, 'hit.wav'))
        self.break_sound = pygame.mixer.Sound(path.join(self.snd_dir, 'break.wav'))
        self.powerup_sound = pygame.mixer.Sound(path.join(self.snd_dir, 'powerup.wav'))

    def reset_game(self):
        """Reset the game state to start a new game."""
        self.paddle = Paddle()
        self.balls = [Ball()]
        self.bricks = []
        self.powerups = []
        self.score = 0
        self.lives = 3
        self.level = 1
        self.create_level()

    def create_level(self):
        """Create a new level with bricks."""
        for row in range(6):
            for col in range(WIDTH // 75):
                tier = min(3, (row // 2) + 1)
                brick = Brick(col * 75, 60 + row * 35, tier)
                self.bricks.append(brick)

    def handle_collisions(self):
        """Handle collisions between the ball, paddle, and bricks."""
        for ball in self.balls:
            # Paddle collision
            if ball.rect.colliderect(self.paddle.rect):
                self.hit_sound.play()
                offset = (ball.rect.centerx - self.paddle.rect.centerx) / (self.paddle.width / 2)
                angle = math.radians(offset * 60 + 90)
                ball.dx = math.cos(angle) * ball.speed
                ball.dy = -math.sin(angle) * ball.speed

            # Brick collisions
            for brick in self.bricks[:]:
                if ball.rect.colliderect(brick.rect):
                    self.hit_sound.play()
                    brick.hits_remaining -= 1
                    if brick.hits_remaining <= 0:
                        self.bricks.remove(brick)
                        self.score += brick.tier * 10
                        self.break_sound.play()
                        if random.random() < 0.25:
                            self.powerups.append(PowerUp(brick.rect.centerx, brick.rect.centery))
                    # Calculate reflection
                    if abs(ball.rect.bottom - brick.rect.top) < 5 and ball.dy > 0:
                        ball.dy *= -1
                    elif abs(ball.rect.top - brick.rect.bottom) < 5 and ball.dy < 0:
                        ball.dy *= -1
                    elif abs(ball.rect.right - brick.rect.left) < 5 and ball.dx > 0:
                        ball.dx *= -1
                    elif abs(ball.rect.left - brick.rect.right) < 5 and ball.dx < 0:
                        ball.dx *= -1

    def handle_powerups(self):
        """Handle power-up movements and collisions with the paddle."""
        for powerup in self.powerups[:]:
            powerup.move()
            if powerup.rect.colliderect(self.paddle.rect):
                self.apply_powerup(powerup)
                self.powerups.remove(powerup)
                self.powerup_sound.play()
            elif powerup.rect.top > HEIGHT:
                self.powerups.remove(powerup)

    def apply_powerup(self, powerup):
        """
        Apply the effect of a power-up.

        Args:
            powerup (PowerUp): The power-up to apply.
        """
        if powerup.type == "expand":
            self.paddle.width = min(200, self.paddle.width + 40)
            self.paddle.rect = pygame.Rect(
                self.paddle.rect.x - 20, self.paddle.rect.y,
                self.paddle.width, self.paddle.height
            )
        elif powerup.type == "slow":
            for ball in self.balls:
                ball.speed = max(4, ball.speed - 2)
        elif powerup.type == "multiball":
            new_ball = Ball()
            new_ball.rect = self.balls[0].rect.copy()
            new_ball.dx = -self.balls[0].dx
            new_ball.dy = self.balls[0].dy
            self.balls.append(new_ball)

    def show_instructions(self):
        """Display game instructions on the screen."""
        instructions = [
            "Welcome to Modern Breakout!",
            "Instructions:",
            "1. Use the LEFT and RIGHT arrow keys to move the paddle.",
            "2. Prevent the ball from falling off the bottom of the screen.",
            "3. Break all the bricks to advance to the next level.",
            "4. Collect power-ups to gain advantages.",
            "Press any key to start the game."
        ]
        self.screen.fill(COLORS["background"])
        for i, line in enumerate(instructions):
            text = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100 + i * 30))
        pygame.display.flip()
        self.wait_for_keypress()

    def wait_for_keypress(self):
        """Wait for the player to press any key."""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False

    def run(self):
        """Main game loop."""
        self.show_instructions()
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.paddle.move("left")
            if keys[pygame.K_RIGHT]:
                self.paddle.move("right")

            for ball in self.balls:
                ball.move()
            self.handle_collisions()
            self.handle_powerups()

            # Check ball loss
            for ball in self.balls[:]:
                if ball.rect.top > HEIGHT:
                    self.balls.remove(ball)
            if not self.balls:
                self.lives -= 1
                if self.lives <= 0:
                    self.reset_game()
                else:
                    self.balls.append(Ball())

            # Check level completion
            if not self.bricks:
                self.level += 1
                self.create_level()
                if self.balls[0].speed < self.balls[0].max_speed:
                    self.balls[0].speed += 0.5
                for ball in self.balls:
                    ball.reset()

            # Drawing
            self.screen.fill(COLORS["background"])
            pygame.draw.rect(self.screen, COLORS["paddle"], self.paddle.rect)
            for ball in self.balls:
                pygame.draw.circle(self.screen, COLORS["ball"], ball.rect.center, ball.radius)

            for brick in self.bricks:
                pygame.draw.rect(self.screen, brick.color, brick.rect)

            for powerup in self.powerups:
                pygame.draw.rect(self.screen, COLORS["powerup"], powerup.rect)

            # UI Elements
            score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            lives_text = self.font.render(f"Lives: {self.lives}", True, (255, 255, 255))
            level_text = self.font.render(f"Level: {self.level}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(lives_text, (WIDTH - 120, 10))
            self.screen.blit(level_text, (WIDTH // 2 - 40, 10))

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()