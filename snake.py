import pygame as PG, config as Config, units as Unit

def draw(window, snake):
    color = {
        'snake': Config.snakeColor,
        'tail': [Config.snakeTailColor[0], Config.snakeTailColor[1]]
    }

    if not snake['isFirstPlayer']:
        color['snake'] = Config.snake2Color
        color['tail'][0] = Config.snake2TailColor[0]
        color['tail'][1] = Config.snake2TailColor[1]

    PG.draw.rect(window, color['snake'], ( Unit.column(snake['x']), Unit.row(snake['y']), Unit.column(1), Unit.row(1) ))

    for i in range(0, len(snake['tail']), 1):
        colorIndex = 0
        tail = snake['tail'][i]

        if i % 2 == 0:
            colorIndex = 1

        PG.draw.rect(window, color['tail'][colorIndex], ( Unit.column(tail['x']), Unit.row(tail['y']), Unit.column(1), Unit.row(1) ))