import pygame as pg
import constants as c
import numpy as np
import drawings
import shapes as sh


def set_background(array: np.ndarray, shapes: list[sh.Shape], score: int, game_over: bool, set_r: bool, uses: int,
                   current_shapes: list[tuple[list[int], str, np.ndarray, int]]):
    c.WIN.fill(c.BLACK)
    pg.draw.rect(c.WIN, c.WHITE, (c.WIDTH, 0, c.SCOREBOARD, c.HEIGHT))
    for idy, y in enumerate(array):
        for idx, x in enumerate(y):
            if x == 0:
                drawings.draw_rect(c.BLACK, idx, idy, False)
            elif x == 1:
                drawings.draw_rect(c.GREY, idx, idy, True)
    for shape in shapes:
        shape()
        shape.shadow()
        if not shape.alive:
            shapes.remove(shape)
    for idx, row in enumerate(array):
        if all(map(lambda s: not s.falling, shapes)) and np.count_nonzero(row == 2) == c.RECTS_X - 2:
            for shape in shapes:
                print(row)
                shape.remove(idx)
            c.REMOVE.play()
            pg.event.post(pg.event.Event(c.SCORE))
    pg.draw.rect(c.WIN, c.BLACK, ((c.RECTS_Y - 9) * (c.RECT_SIDE + c.PAD) - c.PAD,
                                  (c.RECTS_X + 1) * (c.RECT_SIDE + c.PAD) - c.PAD,
                                  8 * (c.RECT_SIDE + c.PAD) + c.PAD, 8 * (c.RECT_SIDE + c.PAD) + c.PAD))
    next_shape, next_color = current_shapes[0][:2]
    next_shape = tuple(map(lambda k: [k[0] + c.RECTS_Y - 7, k[1] + c.RECTS_X - 1], next_shape))
    for s in next_shape:
        drawings.draw_rect(c.COLOR_RGB[next_color], s[1], s[0], True)
    text = c.SCORE_FONT.render(f'Score: {score}', True, c.BLACK)
    c.WIN.blit(text, (c.WIDTH + (c.SCOREBOARD - text.get_width()) // 2, 50))
    n_s = c.NEXT_SHAPE.render('Next shape:', True, c.BLACK)
    c.WIN.blit(n_s, (c.WIDTH + (c.SCOREBOARD - n_s.get_width()) // 2, c.HEIGHT // 2))
    end_text = c.GAME_OVER.render(f'GAME OVER', True, c.RED)
    pg.draw.line(c.WIN, c.RED, (c.RECT_SIDE, (c.RECT_SIDE + c.PAD) * 3 - c.PAD),
                 (c.WIDTH - c.PAD - c.RECT_SIDE, (c.RECT_SIDE + c.PAD) * 3 - c.PAD))
    if score % 500 == 0 and score > 0:
        pg.event.post(pg.event.Event(c.CRUSH))
    if set_r:
        upgrade = c.SCORE_FONT.render('Press \'R\'', True, c.BLACK)
        upgrade_ = c.SUB_FONT.render('to remove lowest row', True, c.BLACK)
        c.WIN.blit(upgrade, (c.WIDTH + (c.SCOREBOARD - upgrade.get_width()) // 2, c.HEIGHT // 2 - upgrade.get_height() -
                             upgrade_.get_height()))
        c.WIN.blit(upgrade_, (c.WIDTH + (c.SCOREBOARD - upgrade_.get_width()) // 2, c.HEIGHT // 2 - upgrade_.get_height()))
        if uses > 1:
            use = c.SUB_FONT.render(f'{uses}x', True, c.BLACK)
            c.WIN.blit(use, (c.WIDTH + (c.SCOREBOARD - use.get_width()) // 2, 330))
    if game_over:
        c.WIN.blit(end_text, ((c.WIDTH + c.SCOREBOARD - end_text.get_width()) // 2, (c.HEIGHT - end_text.get_height())
                              // 2))
    pg.display.update()