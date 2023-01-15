import pygame as pg
import constants as c


def set_menu(play: pg.Surface, rect: tuple, options: pg.Surface, options_rect: tuple):
    c.WIN.fill(c.WHITE)
    entry = c.WELCOME.render('WELCOME TO TETRIS', True, c.BLACK)
    c.WIN.blit(entry, ((c.WIN.get_width() - entry.get_width()) // 2, (c.WIN.get_height() - entry.get_height()) // 2 - 200))

    play_x = c.WIN.get_width() // 2 - play.get_width() // 2
    play_y = c.WIN.get_height() // 2 - play.get_height() // 2
    pg.draw.rect(c.WIN, c.BLACK, (rect[1][0] - c.PAD, rect[1][1] - c.PAD, rect[1][2] + 2 * c.PAD, rect[1][3] + 2 * c.PAD))
    pg.draw.rect(c.WIN, *rect)
    c.WIN.blit(play, (play_x, play_y + 200))

    options_x = c.WIN.get_width() // 2 - options.get_width() // 2
    options_y = c.WIN.get_height() // 2 - options.get_height() // 2
    pg.draw.rect(c.WIN, options_rect[0], options_rect[1])
    c.WIN.blit(options, (options_x, options_y))
    pg.display.update()
