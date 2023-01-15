import pygame as pg
import constants as c


def draw_rect(color: tuple[int, int, int], x: int, y: int, border: bool) -> None:
    if border:
        pg.draw.rect(c.WIN, color, (x * (c.RECT_SIDE + c.PAD), y * (c.RECT_SIDE + c.PAD), c.RECT_SIDE, c.RECT_SIDE),
                     border_radius=c.PAD)
        return
    pg.draw.rect(c.WIN, color, (x * (c.RECT_SIDE + c.PAD), y * (c.RECT_SIDE + c.PAD), c.RECT_SIDE + c.PAD, c.RECT_SIDE +
                                c.PAD), )
