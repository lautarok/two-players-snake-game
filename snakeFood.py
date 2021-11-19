import pygame as PG, colors as Color, units as Unit

def draw(window, generated):
    PG.draw.rect(window, Color.white, ( Unit.column(generated['x']), Unit.row(generated['y']), Unit.column(1), Unit.row(1) ))