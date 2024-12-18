from turtle import Turtle


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.score_l = 0
        self.score_r = 0
        self.update_scoreboard()

    def update_scoreboard(self):
        self.goto(0, 200)
        self.write(f"{self.score_l} : {self.score_r}", False, "center", ("Courier", 80, "normal"))

    def l_point(self):
        self.score_l += 1
        self.clear()
        self.update_scoreboard()

    def r_point(self):
        self.score_r += 1
        self.clear()
        self.update_scoreboard()

