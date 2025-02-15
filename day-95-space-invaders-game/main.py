import turtle
import time
import random

# Set up screen
screen = turtle.Screen()
screen.title("Space Invaders")
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.tracer(0)

# Player ship
player = turtle.Turtle()
player.color("blue")
player.shape("triangle")
player.shapesize(1.5, 1.5)
player.penup()
player.goto(0, -250)
player_speed = 20
bullet_state = "ready"

# Aliens
aliens = []
alien_speed = 0.5
alien_direction = 1

# Barriers
barriers = []

# Score
score = 0
score_display = turtle.Turtle()
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(-380, 260)
score_display.write(f"Score: {score}", font=("Courier", 14, "normal"))


def create_aliens():
    for y in range(200, 100, -50):
        for x in range(-300, 300, 60):
            alien = turtle.Turtle()
            alien.color("green")
            alien.shape("circle")
            alien.shapesize(1.2, 1.2)
            alien.penup()
            alien.goto(x, y)
            aliens.append(alien)


def create_barriers():
    for x in [-300, -100, 100, 300]:
        barrier = turtle.Turtle()
        barrier.color("gray")
        barrier.shape("square")
        barrier.shapesize(4, 4)
        barrier.penup()
        barrier.goto(x, -200)
        barriers.append(barrier)


def move_left():
    x = player.xcor()
    if x > -380:
        x -= player_speed
    player.setx(x)


def move_right():
    x = player.xcor()
    if x < 380:
        x += player_speed
    player.setx(x)


def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        bullet = turtle.Turtle()
        bullet.color("yellow")
        bullet.shape("triangle")
        bullet.shapesize(0.5, 0.5)
        bullet.penup()
        bullet.goto(player.xcor(), player.ycor() + 20)
        bullet.setheading(90)

        while bullet.ycor() < 275:
            bullet.forward(20)
            screen.update()

            # Check collisions
            for alien in aliens:
                if abs(bullet.xcor() - alien.xcor()) < 20 and abs(bullet.ycor() - alien.ycor()) < 20:
                    alien.goto(1000, 1000)
                    aliens.remove(alien)
                    bullet.hideturtle()
                    global score
                    score += 10
                    score_display.clear()
                    score_display.write(f"Score: {score}", font=("Courier", 14, "normal"))
                    return

            time.sleep(0.01)

        bullet.hideturtle()
        bullet_state = "ready"


def move_aliens():
    global alien_direction
    move_down = False

    for alien in aliens:
        x = alien.xcor()
        x += alien_speed * alien_direction
        alien.setx(x)

        if x > 380 or x < -380:
            move_down = True

    if move_down:
        alien_direction *= -1
        for alien in aliens:
            y = alien.ycor()
            y -= 40
            alien.sety(y)

        # Check game over
        if alien.ycor() < -220:
            game_over("ALIENS INVADED!")


def game_over(message):
    screen.clear()
    screen.bgcolor("black")
    game_over_display = turtle.Turtle()
    game_over_display.color("red")
    game_over_display.penup()
    game_over_display.write(message, align="center", font=("Courier", 24, "normal"))
    screen.update()
    time.sleep(3)
    turtle.bye()


# Keyboard bindings
screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(fire_bullet, "space")

# Create game elements
create_aliens()
create_barriers()

# Main game loop
while True:
    screen.update()

    # Check for alien attacks
    if random.randint(0, 100) < 2 and len(aliens) > 0:
        attacker = random.choice(aliens)
        bullet = turtle.Turtle()
        bullet.color("red")
        bullet.shape("circle")
        bullet.shapesize(0.5)
        bullet.penup()
        bullet.goto(attacker.xcor(), attacker.ycor())
        bullet.setheading(-90)

        while bullet.ycor() > -275:
            bullet.forward(10)
            screen.update()

            # Check player hit
            if abs(bullet.xcor() - player.xcor()) < 20 and abs(bullet.ycor() - player.ycor()) < 20:
                game_over("GAME OVER!")

            time.sleep(0.01)

        bullet.hideturtle()

    move_aliens()

    # Check win condition
    if len(aliens) == 0:
        game_over("YOU WIN!")

    time.sleep(0.01)