import pygame as pg
import constants as c


def set_option(back: pg.Surface, speed: pg.Surface, hovering: bool, up: pg.Surface, down: pg.Surface, game_speed: int):
    c.WIN.fill(c.CYAN)
    c.WIN.blit(back, (c.WIN.get_width() // 2 - back.get_width() // 2, 0))

    speed_x = c.WIN.get_width() // 2 - speed.get_width() // 2
    speed_y = 100

    fps = c.GAME_SPEED.render(f'FPS at {game_speed}', True, c.BLACK)
    fps_x = c.WIN.get_width() // 2 - fps.get_width() // 2
    fps_y = 150

    c.WIN.blit(speed, (speed_x, speed_y))
    if hovering:
        c.WIN.blit(up, (speed_x - 50, speed_y + speed.get_height() // 3))
        c.WIN.blit(down, (speed_x + speed.get_width() + 10, speed_y + speed.get_height() // 3))
        c.WIN.blit(fps, (fps_x, fps_y))
    pg.display.update()
