import pygame as pg
import numpy as np
import os
import constants as c
import random
import shapes as sh
import menu
import options as op
import background
pg.init()
pg.mixer.init()


def main():
    run = True
    pre_run = True
    clock = pg.time.Clock()

    pg.display.set_caption('Tetris')
    pg.display.set_icon(pg.image.load(os.path.join('Assets', 'red_block.png')))

    play = c.PLAY.render('PLAY', True, c.WHITE)
    play_x = c.WIN.get_width() // 2 - play.get_width() // 2
    play_y = c.WIN.get_height() // 2 - play.get_height() // 2 + 200

    options = c.OPTIONS.render('OPTIONS', True, c.BLACK)
    options_x = c.WIN.get_width() // 2 - options.get_width() // 2
    options_y = c.WIN.get_height() // 2 - options.get_height() // 2

    back = c.BACK.render('BACK', True, c.RED)
    back_x = c.WIN.get_width() // 2 - back.get_width() // 2
    back_y = 0

    speed = c.SPEED.render('GAME SPEED', True, c.BLACK)
    speed_x = c.WIN.get_width() // 2 - speed.get_width() // 2
    speed_y = 100

    up, down = pg.transform.scale(pg.image.load(os.path.join('Assets', 'unclicked_up.png')), (40, 20)),\
        pg.transform.scale(pg.image.load(os.path.join('Assets', 'unclicked_down.png')), (40, 20))

    game_speed = c.FPS

    board = np.ones((c.RECTS_Y, c.RECTS_X), dtype='int32')
    board[1:c.RECTS_Y - 1, 1:c.RECTS_X - 1].fill(0)
    shapes = []
    current_shapes = []
    track = pg.mixer.Sound(os.path.join('Assets', 'theme.mp3'))
    track.play(-1)
    score = 0
    counter = 0
    game_over = False
    new_game = False
    set_r = False
    usage = False
    uses = 0
    pause = False
    clicked = False
    # MAIN MENU
    while pre_run:
        clock.tick(game_speed)
        x_pos, y_pos = pg.mouse.get_pos()
        if clicked:
            pre_run = False
        if 0 <= x_pos - play_x <= play.get_width() and 0 <= y_pos - play_y <= play.get_height():
            play = c.PLAY.render('PLAY', True, c.BLUE)
            rect = c.CYAN, (play_x, play_y, play.get_width(), play.get_height())
        else:
            play = c.PLAY.render('PLAY', True, c.WHITE)
            rect = c.BLUE, (play_x, play_y, play.get_width(), play.get_height())
        if 0 <= x_pos - options_x <= options.get_width() and 0 <= y_pos - options_y <= options.get_height():
            options = c.OPTIONS.render('OPTIONS', True, c.BLUE)
            options_rect = c.WHITE, (options_x, options_y, options.get_width(), options.get_height())
        else:
            options = c.OPTIONS.render('OPTIONS', True, c.BLACK)
            options_rect = c.WHITE, (options_x, options_y, options.get_width(), options.get_height())
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pre_run = False
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pre_run = False
                    run = False
                if event.key == pg.K_RETURN:
                    pre_run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = event.pos
                if play_x <= x <= play_x + play.get_width() and play_y <= y <= play_y + play.get_height() and event.button == pg.BUTTON_LEFT:
                    clicked = True
                if 0 <= x - options_x <= options.get_width() and 0 <= y - options_y <= options.get_height() and event.button == pg.BUTTON_LEFT:
                    set_options = True
                    # OPTIONS MENU
                    while set_options:
                        clock.tick(game_speed)
                        x_pos, y_pos = pg.mouse.get_pos()
                        if 0 <= x_pos - back_x <= back.get_width() and 0 <= y_pos - back_y <= back.get_height():
                            back = c.BACK.render('BACK', True, c.BLACK)
                        else:
                            back = c.BACK.render('BACK', True, c.RED)
                        if -50 <= x_pos - speed_x <= speed.get_width() + 50 and 0 <= y_pos - speed_y <= speed.get_height():
                            speed = c.SPEED.render('GAME SPEED', True, c.BLUE)
                            hovering = True
                            if -50 <= x_pos - speed_x <= -10:
                                up = pg.transform.scale(pg.image.load(os.path.join('Assets', 'hovered_up.png')), (40, 20))
                            else:
                                up = pg.transform.scale(pg.image.load(os.path.join('Assets', 'unclicked_up.png')), (40, 20))
                            if 10 <= x_pos - speed_x - speed.get_width() <= 50:
                                down = pg.transform.scale(pg.image.load(os.path.join('Assets', 'hovered_down.png')), (40, 20))
                            else:
                                down = pg.transform.scale(pg.image.load(os.path.join('Assets', 'unclicked_down.png')),
                                                          (40, 20))

                        else:
                            speed = c.SPEED.render('GAME SPEED', True, c.BLACK)
                            hovering = False
                        for event_1 in pg.event.get():
                            if event_1.type == pg.QUIT:
                                set_options = False
                                pre_run = False
                                run = False
                            if event_1.type == pg.MOUSEBUTTONDOWN:
                                x, y = event_1.pos
                                if 0 <= x - back_x <= back.get_width() and 0 <= y - back_y <= back.get_height() and\
                                        event_1.button == pg.BUTTON_LEFT:
                                    set_options = False
                                if -50 <= x - speed_x <= -10 and event.button == pg.BUTTON_LEFT:
                                    up = pg.transform.scale(pg.image.load(os.path.join('Assets', 'clicked_up.png')), (40, 20))
                                    game_speed += 10
                                if 10 <= x_pos - speed_x - speed.get_width() <= 50:
                                    down = pg.transform.scale(pg.image.load(os.path.join('Assets', 'clicked_down.png')), (40, 20))
                                    if game_speed > 10:
                                        game_speed -= 10
                        op.set_option(back, speed, hovering, up, down, game_speed)
        if pre_run:
            menu.set_menu(play, rect, options, options_rect)
    # GAME
    while run:
        clock.tick(game_speed)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
                if event.key == pg.K_RIGHT and not pause:
                    for shape in shapes:
                        shape.move(1)
                if event.key == pg.K_LEFT and not pause:
                    for shape in shapes:
                        shape.move(-1)
                if event.key == pg.K_RETURN and not pause:
                    for shape in shapes:
                        shape.flip()
                if event.key == pg.K_r and set_r and not pause:
                    for shape in shapes:
                        shape.remove(c.RECTS_Y - 2)
                    set_r = False
                    usage = True
                    uses -= 1
                    c.REMOVE.play()
                if event.key == pg.K_q:
                    score += 100
                if event.key == pg.K_p:
                    pause = not pause
                if event.key == pg.K_TAB and not pause:
                    for shape in shapes:
                        shape.smash()
                if event.key == pg.K_SPACE:
                    run = False
                    track.stop()
                    new_game = True
            if event.type == c.SCORE:
                score += 100
            if event.type == c.CRUSH and not usage:
                set_r = True
                usage = True
                c.R.play()
        if score % 500 > 0 and usage:
            usage = False
        if all(map(lambda s: not s.falling, shapes)) and 2 in board[:3]:
            track.stop()
            game_over = True
        if all(map(lambda s: not s.falling, shapes)) and not game_over:
            shape_0 = random.choice(c.SHAPES)
            color_0 = random.choice(c.COLORS)
            start = 0
            if shape_0 == ([1, 4], [1, 5], [1, 6], [1, 7]):
                start = 1
            current_shapes.insert(0, (shape_0, color_0, board, start))
            if len(current_shapes) == 1:
                shape_1 = random.choice(c.SHAPES)
                color_1 = random.choice(c.COLORS)
                start_1 = 0
                if shape_1 == ([1, 4], [1, 5], [1, 6], [1, 7]):
                    start_1 = 1
                current_shapes.insert(0, (shape_1, color_1, board, start_1))
            if len(current_shapes) == 3:
                current_shapes.pop()
            print(list(map(lambda s: s.falling, shapes)).count(True))
            shapes.append(sh.Shape(*current_shapes[-1]))
        if counter % 15 == 0 and not pause:
            background.set_background(board, shapes, score, game_over, set_r, uses, current_shapes)
        if new_game:
            main()
        if counter < c.FPS - 1:
            counter += 1
        else:
            counter = 0


if __name__ == '__main__':
    main()
