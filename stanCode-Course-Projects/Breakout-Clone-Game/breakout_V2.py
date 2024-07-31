"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

Add timer, score board, and lives board for the game.
"""

from campy.gui.events.timer import pause
from extension_breakoutgraphics import BreakoutGraphics
from campy.gui.events.mouse import onmouseclicked, onmousemoved

FRAME_RATE = 10         # 100 frames per second
NUM_LIVES = 3			# Number of attempts


def main():
    graphics = BreakoutGraphics()
    current_lives = NUM_LIVES
    graphics.welcome_screen()

    # Add the animation loop here
    while True:
        if current_lives > 0:
            graphics.ball_move()
        pause(FRAME_RATE)


if __name__ == '__main__':
    main()
