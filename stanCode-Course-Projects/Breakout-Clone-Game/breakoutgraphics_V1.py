"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Width of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 75      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball
BG_COLOR = 'cadetblue'  # add by myself, background color for the window

is_waiting_click = True  # control whether it's waiting mouseclick or not
is_in_game = False  # control if it's in game or not
need_change_velocity = True  # 問助教：velocity改變的方法是否正確


class BreakoutGraphics:
    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        # Create a graphical window, with some extra space
        self._window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        self._window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self._window = GWindow(width=self._window_width, height=self._window_height, title=title)

        # background of window
        self.bg_color = GRect(self._window_width, self._window_height)
        self.bg_color.fill_color = BG_COLOR
        self.bg_color.color = BG_COLOR
        self.bg_color.filled = True
        self._window.add(self.bg_color)

        # Create a paddle
        # center of paddle = center of window, distance between paddle and window's bottom = PADDLE_OFFSET
        self._paddle_width = paddle_width
        self._paddle_height = paddle_height
        self._paddle = GRect(paddle_width, paddle_height, x=(self._window_width - paddle_width)/2,
                             y=(self._window_height - paddle_offset - paddle_height))
        self._paddle.filled = True
        self._paddle.fill_color = 'thistle'
        self._paddle.color = self._paddle.fill_color
        self._window.add(self._paddle)

        # Center a filled ball in the graphical window
        self._ball_width = ball_radius*2
        self._ball_height = ball_radius*2
        self._ball = GOval(ball_radius*2, ball_radius*2,
                           x=(self._window_width - self._ball_width) / 2 - self._ball_width,
                           y=(self._window_height - self._ball_height) / 2 - self._ball_height)
        self._ball.filled = True
        self._ball.fill_color = 'gold'
        self._ball.color = self._ball.fill_color
        self._window.add(self._ball)

        self._ball_corner_1 = (0, 0)  # top-left
        self._ball_corner_2 = (0, 0)  # top-right
        self._ball_corner_3 = (0, 0)  # bottom-left
        self._ball_corner_4 = (0, 0)  # bottom-right

        # Draw bricks (different colors)
        self._bricks = []
        for i in range(brick_rows):
            for j in range(brick_cols):
                brick = GRect(brick_width, brick_height)
                brick.filled = True
                if i < 2:
                    brick.color = 'salmon'
                elif i < 4:
                    brick.color = 'lightsalmon'
                elif i < 6:
                    brick.color = 'lightpink'
                elif i < 8:
                    brick.color = 'lavenderblush'
                else:
                    brick.color = 'ivory'
                brick.fill_color = brick.color
                self._window.add(brick, x=j * (brick_width + brick_spacing),
                                 y=brick_offset + i * (brick_height + brick_spacing))
                self._bricks.append(brick)

        # Initialize variables
        self._dx = 0  # horizontal velocity of ball
        self._dy = 0  # vertical velocity of ball
        self.lives = 3
        self.score = 0
        self.score_list = []
        self._remove_bricks_count = 0

        # start btn - start_btn_bg
        self.start_btn_bg_width = 100
        self.start_btn_bg_height = 60
        self.start_btn_bg = GRect(100, 60, x=(self._window_width - self.start_btn_bg_width)/2,
                                  y=(self._window_height - self.start_btn_bg_height)/2)
        self.start_btn_bg.filled = True
        self.start_btn_bg.color = 'Red'
        self.start_btn_bg.fill_color = 'Red'

        onmouseclicked(self.start_game_click)
        onmousemoved(self.start_game_move)

    def start_game_click(self, mouse):
        """
        mouse listener, onmouseclicked work, only when is_start_click == True
        onmouseclicked() check whether the mouse clicked start_btn
        when clicked start_btn, switch is_start_click to False, then the rest mouse clicks in the game won't be counted
        """
        global is_waiting_click
        global is_in_game
        # global is_timer_on
        if is_waiting_click:
            mouse_get = self._window.get_object_at(mouse.x, mouse.y)
            if mouse_get is not None:
                is_waiting_click = False
                is_in_game = True

    def start_game_move(self, mouse):
        """
        mouse listner, onmousemoved() work, only when is_start_click == False
        onmousemoved() controls paddle's move (the paddle moves when the game started
        """
        if mouse.x > self._window.width-0.5*self._paddle.width:
            self._paddle.x = self._window.width - self._paddle.width
        # paddle move - left side
        elif mouse.x < 0.5*self._paddle.width:
            self._paddle.x = 0
        # paddle move - middle
        elif 0.5*self._paddle.width <= mouse.x <= self._window.width - 0.5*self._paddle.width:
            self._paddle.x = mouse.x - 0.5*self._paddle.width

    def set_ball_init_velocity(self):
        """
        initialize ball's horizontal and vertical value
        """
        self._dx = random.randint(1, MAX_X_SPEED)
        self._dy = INITIAL_Y_SPEED
        if random.random() > 0.5:
            self._dx = -self._dx
        if random.random() > 0.5:
            self._dy = -self._dy

    def ball_move(self):
        """
        control ball's everything
        """
        global is_waiting_click
        global need_change_velocity
        global is_in_game
        global is_waiting_click
        if is_in_game:
            if need_change_velocity:
                self.set_ball_init_velocity()
                need_change_velocity = False
            self._ball.move(self._dx, self._dy)
            self.check_collision()

            # if ball out of window
            if self._ball.y + self._ball.height >= self._window.height:
                self.score_list.append(self.score)
                self.lives -= 1
                self._window.remove(self._ball)
                if self.lives > 0:
                    self.init_when_end_game()
                    is_waiting_click = True
                else:
                    is_in_game = False
                    self.game_over()

    def init_when_end_game(self):
        """
        things need to do when game ends (except game over)
        """
        global is_in_game
        self.score = 0
        self._remove_bricks_count = 0
        is_in_game = False
        # reset ball
        self.reset_ball_position()
        self.set_ball_init_velocity()
        self._window.add(self._ball)

    def reset_ball_position(self):
        """
        reset ball's position to the center of the window
        """
        self._ball.x = (self._window_width - self._ball.width) / 2 - 0.5*self._ball.width
        self._ball.y = (self._window_height - self._ball.height) / 2 - 0.5*self._ball.height

    def reset_paddle_position(self):
        """
        reset paddle's position
        """
        self._paddle.x = (self._window_width - self._paddle_width)/2
        self._paddle.y = self._window_height - PADDLE_OFFSET - self._paddle_height

    def check_collision(self):
        self.check_collision_with_window()  # detect anytime
        if self.detect_collision():
            self.check_collision_with_paddle()  # detect only when any of four corners of the ball isn't none
            self.check_collision_with_bricks()  # detect only when any of four corners of the ball isn't none

    def detect_collision(self):
        """
        Check if the ball's corners have collided with any object.
        """
        return any(self._window.get_object_at(*corner) is not None for corner in self.get_ball_corners())

    def get_ball_corners(self):
        """
        Get the four corners of the ball.
        """
        self._ball_corner_1 = (self._ball.x, self._ball.y)  # top-left
        self._ball_corner_2 = (self._ball.x + self._ball.width, self._ball.y)  # top-right
        self._ball_corner_3 = (self._ball.x, self._ball.y + self._ball.height)  # bottom-left
        self._ball_corner_4 = (self._ball.x + self._ball.width, self._ball.y + self._ball.height)  # bottom-right

        return [
            self._ball_corner_1,  # top-left
            self._ball_corner_2,  # top-right
            self._ball_corner_3,  # bottom-left
            self._ball_corner_4  # bottom-right
        ]

    def check_collision_with_window(self):
        """
        Check collision with window edges.
        """
        if self._ball.x <= 0 or self._ball.x + self._ball.width >= self._window.width:
            self._dx = -self._dx
        if self._ball.y <= 0:
            self._dy = -self._dy

    def check_collision_with_paddle(self):
        """
        Check collision with paddle.
        reminder: can't judge by ==, otherwise, the ball will penetrate through the paddle
        """

        # check collision with paddle - north of paddle
        if self._dy > 0:
            if self._ball_corner_3 in self._paddle or self._ball_corner_4 in self._paddle:
                self._dy = - self._dy

        # check collision with paddle - west of paddle
        if self._dx > 0:
            if self._ball_corner_2 in self._paddle or self._ball_corner_4 in self._paddle:
                self._dx = - self._dx

        # check collision with paddle - east of paddle
        if self._dx < 0:
            if self._ball_corner_1 in self._paddle or self._ball_corner_3 in self._paddle:
                self._dx = - self._dx

    def check_collision_with_bricks(self):
        """
        Check collision with bricks, add score if bricks are hit
        """
        for corner in self.get_ball_corners():
            obj = self._window.get_object_at(*corner)
            if obj is not None and obj in self._bricks:
                self._dy = -self._dy
                self._window.remove(obj)
                self._bricks.remove(obj)
                self.score += 10
                if len(self._bricks) == 0:
                    self.game_win()
                break

    def game_win(self):
        """
        when length of bricks == 0, user wins the game
        """
        global is_in_game
        is_in_game = False
        self._window.clear()
        self._window.add(self.bg_color)
        game_over_label = GLabel(f'Congrats!\n\nYou\'ve won!')
        game_over_label.font = 'Helvetica-36-bold'
        game_over_label.color = 'Gold'
        self._window.add(game_over_label, 20, (self._window_height + game_over_label.height) / 2 - 20)

    def game_over(self):
        """
        when lives = 0, clear window, shows highest score
        """
        self._window.clear()
        self._window.add(self.bg_color)
        game_over_label = GLabel(f'Game Over\n\nHighest Score: {max(self.score_list)}')
        game_over_label.font = 'Helvetica-36-bold'
        game_over_label.color = 'Gold'
        self._window.add(game_over_label, 20, (self._window_height + game_over_label.height) / 2 - 20)
