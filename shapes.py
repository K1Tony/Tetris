import pygame as pg
import constants as c
import numpy as np
import os
import drawings


def increment(table: list[list[int]]):
    for box in table:
        box[0] -= 1
    return table


def find_lowest(array: np.ndarray, coordinates: tuple[list[int]], lowest: int, get_diff: bool) -> list[list[int]] | int:
    result = []
    pre_result = []
    for y, x in coordinates:
        for idy, row in enumerate(array[:, x]):
            if row == 2 and [idy, x] not in coordinates and idy > y:
                pre_result.append(idy - 1 - y)
    if pre_result:
        diff = min(pre_result)
    else:
        diff = c.RECTS_Y - lowest - 2
    if get_diff:
        return diff
    if diff == 0:
        return result
    for y, x in coordinates:
        y_ = y + diff
        result.append([y_, x])
    if any(map(lambda k: k[0] > c.RECTS_Y - 2, result)):
        result = increment(result)
    return result


class Shape:
    blocks = {
        'green': pg.transform.scale(pg.image.load(os.path.join('Assets', 'green_block.png')), (c.RECT_SIDE, c.RECT_SIDE)),
        'blue': pg.transform.scale(pg.image.load(os.path.join('Assets', 'blue_block.png')), (c.RECT_SIDE, c.RECT_SIDE)),
        'cyan': pg.transform.scale(pg.image.load(os.path.join('Assets', 'cyan_block.png')), (c.RECT_SIDE, c.RECT_SIDE)),
        'orange': pg.transform.scale(pg.image.load(os.path.join('Assets', 'orange_block.png')), (c.RECT_SIDE, c.RECT_SIDE)),
        'purple': pg.transform.scale(pg.image.load(os.path.join('Assets', 'purple_block.png')), (c.RECT_SIDE, c.RECT_SIDE)),
        'red': pg.transform.scale(pg.image.load(os.path.join('Assets', 'red_block.png')), (c.RECT_SIDE, c.RECT_SIDE)),
        'yellow': pg.transform.scale(pg.image.load(os.path.join('Assets', 'yellow_block.png')), (c.RECT_SIDE, c.RECT_SIDE))
    }

    def __init__(self, coordinates: tuple[list[int], list[int], list[int], list[int]], color: str, board: np.ndarray, side: int):
        self.coordinates = [coord[::] for coord in coordinates]
        self.rects = list(map(lambda x: pg.Rect(x[1] * (c.RECT_SIDE + c.PAD), x[0] * (c.RECT_SIDE + c.PAD), c.RECT_SIDE,
                                                c.RECT_SIDE), self.coordinates))
        self.color = color
        self.board = board
        self.side = side
        self.height = len(set(map(lambda x: x[0], self.coordinates)))
        self.width = len(set(map(lambda x: x[1], self.coordinates)))
        self.length = max(self.width, self.height)
        self.falling = True
        self.blocks_falling = [True for _ in self.coordinates]
        self.alive = True
        for coord in self.coordinates:
            self.board[tuple(coord)] = 2
        self.highest = min(map(lambda x: x[0], self.coordinates))
        self.lowest = max(map(lambda x: x[0], self.coordinates))
        self.far_right = max(map(lambda x: x[1], self.coordinates))
        self.far_left = min(map(lambda x: x[1], self.coordinates))
        if self.lowest == c.RECTS_Y - 1:
            self.lowest += 1
        self.lowest_point = find_lowest(self.board, tuple(self.coordinates), self.lowest, False)
        self.called_remove = 0

    def redefine(self, cond: bool):
        self.rects = list(map(lambda x: pg.Rect(x[1] * (c.RECT_SIDE + c.PAD), x[0] * (c.RECT_SIDE + c.PAD), c.RECT_SIDE,
                                                c.RECT_SIDE), self.coordinates))
        self.height = len(set(map(lambda x: x[0], self.coordinates)))
        self.width = len(set(map(lambda x: x[1], self.coordinates)))
        self.length = max(self.width, self.height)
        self.falling = True
        if cond:
            for coord in self.coordinates:
                self.board[tuple(coord)] = 2
        self.highest = min(map(lambda x: x[0], self.coordinates))
        self.lowest = max(map(lambda x: x[0], self.coordinates))
        self.far_right = max(map(lambda x: x[1], self.coordinates))
        self.far_left = min(map(lambda x: x[1], self.coordinates))
        if self.lowest == c.RECTS_Y - 1:
            self.lowest += 1
        self.lowest_point = find_lowest(self.board, tuple(self.coordinates), self.lowest, False)

    def __repr__(self):
        return f'{self.coordinates}'

    def __call__(self):
        if self.alive:
            for rect, coord in zip(self.rects, self.coordinates):
                if self.board[tuple(coord)] == 2:
                    c.WIN.blit(self.blocks[self.color], (rect.x, rect.y))
            for y, x in self.coordinates:
                if y == 20:
                    self.falling = False
                    return
                if self.board[y, x] == 2 and self.board[y + 1, x] > 0 and [y + 1, x] not in self.coordinates:
                    self.falling = False
                    return
            for coord in self.coordinates:
                self.board[tuple(coord)] = 0
            for rect, coord in zip(self.rects, self.coordinates):
                rect.y += c.RECT_SIDE + c.PAD
                coord[0] += 1
                self.board[tuple(coord)] = 2
            self.height = len(set(map(lambda k: k[0], self.coordinates)))
            self.width = len(set(map(lambda k: k[1], self.coordinates)))
            self.length = max(self.width, self.height)
            self.highest = min(map(lambda k: k[0], self.coordinates))
            self.lowest = max(map(lambda k: k[0], self.coordinates))
            self.far_right = max(map(lambda k: k[1], self.coordinates))
            self.far_left = min(map(lambda k: k[1], self.coordinates))
            if self.lowest == c.RECTS_Y - 1:
                self.lowest += 1
            self.lowest_point = find_lowest(self.board, tuple(self.coordinates), self.lowest, False)

    def move(self, right: 1 | -1) -> None:
        if self.falling:
            for coord in self.coordinates:
                y, x = coord
                if self.board[y, x + right] in [1, 2] and [y, x + right] not in self.coordinates:
                    return
            for coord in self.coordinates:
                self.board[tuple(coord)] = 0
            for rect, coord in zip(self.rects, self.coordinates):
                rect.x += right * (c.RECT_SIDE + c.PAD)
                coord[1] += right
                self.board[tuple(coord)] = 2

    def flip(self) -> None:
        if self.falling and self.highest < c.RECTS_Y - 1 - self.length and self.far_left < c.RECTS_X - 1 - self.length\
                and self.side in [0, 1]:
            sty = self.highest
            eny = self.highest + self.length
            stx = self.far_left
            enx = self.far_left + self.length
            square = self.board[sty:eny, stx:enx]
            condition = True
            for idy, row in enumerate(square):
                for idx, col in enumerate(row):
                    if [idy + sty, idx + stx] not in self.coordinates and col == 2:
                        condition = False
            if condition:
                if self.side == 0:
                    self.board[sty:eny, stx:enx] = np.fliplr(self.board[sty:eny, stx:enx].T)
                    self.coordinates.clear()
                    for idy, y in enumerate(square):
                        for idx, x in enumerate(y):
                            if x == 2:
                                self.coordinates.append([idy + sty, idx + stx])
                    self.side = 1
                    self.redefine(True)
                elif self.side == 1:
                    self.board[sty:eny, stx:enx] = np.fliplr(self.board[sty:eny, stx:enx].T)
                    self.coordinates.clear()
                    for idy, y in enumerate(square):
                        for idx, x in enumerate(y):
                            if x == 2:
                                self.coordinates.append([idy + sty, idx + stx])
                    self.side = 2
                    self.redefine(True)
        elif self.falling and self.lowest < c.RECTS_Y - 2 and self.far_left > 1:
            sty = self.lowest - self.length + 1
            eny = self.lowest + 1
            stx = self.far_right - self.length + 1
            enx = self.far_right + 1
            square = self.board[sty:eny, stx:enx]
            condition = True
            for idy, row in enumerate(square):
                for idx, col in enumerate(row):
                    if [idy + sty, idx + stx] not in self.coordinates and col in [1, 2]:
                        condition = False
            if condition:
                if self.side == 2:
                    self.board[sty:eny, stx:enx] = np.fliplr(self.board[sty:eny, stx:enx].T)
                    self.coordinates.clear()
                    for idy, y in enumerate(square):
                        for idx, x in enumerate(y):
                            if x == 2:
                                self.coordinates.append([idy + sty, idx + stx])
                    self.side = 3
                    self.redefine(True)
                elif self.side == 3:
                    self.board[sty:eny, stx:enx] = np.fliplr(self.board[sty:eny, stx:enx].T)
                    self.coordinates.clear()
                    for idy, y in enumerate(square):
                        for idx, x in enumerate(y):
                            if x == 2:
                                self.coordinates.append(
                                    [idy + sty, idx + stx])
                    self.side = 0
                    self.redefine(True)

    def remove(self, row: int) -> None:
        self.board[row].fill(0)
        self.board[row, 0] = self.board[row, c.RECTS_X - 1] = 1
        print(self.board)
        self.coordinates = [coord for coord in self.coordinates if self.board[tuple(coord)] == 2]
        if self.coordinates:
            self.redefine(True)
        else:
            self.alive = False

    def shadow(self):
        if self.falling and self.lowest_point:
            for y, x in self.lowest_point:
                drawings.draw_rect(c.DIMMER[self.color], x, y, True)

    def smash(self):
        if self.falling and self.lowest_point:
            for coord in self.coordinates:
                self.board[tuple(coord)] = 0
            self.coordinates = self.lowest_point
            self.redefine(True)
            c.SMASH.play()