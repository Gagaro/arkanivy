from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock


class ArkanivyPaddle(Widget):
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(vx, -1 * vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class ArkanivyBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class ArkanivyGame(Widget):
    ball = ObjectProperty(None)
    player = ObjectProperty(None)

    def serve_ball(self, vel=(1, 2)):
        self.ball.center_x = self.center_x
        self.ball.center_y = self.y + 75
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        self.player.bounce_ball(self.ball)

        # bounce ball off size
        if self.ball.top > self.top:
            self.ball.velocity_y *= -1
        if self.ball.x < self.x or self.ball.x + self.ball.width > self.width:
            self.ball.velocity_x *= -1

        # went of to bottom
        if self.ball.y < self.y:
            self.serve_ball()

    def on_touch_move(self, touch):
        self.player.center_x = touch.x


class ArkanivyApp(App):
    def build(self):
        game = ArkanivyGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    ArkanivyApp().run()
