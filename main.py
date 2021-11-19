import sys as System
import pygame as PG
import colors as Color
import config as Config
import snake as Snake
import snakeFood as SnakeFood
import random

snake = {
	'x': Config.displayColumns / 2,
	'y': Config.displayRows / 2,
	'direction': False,
	'tail': [
		{
			'x': Config.displayColumns / 2,
			'y': (Config.displayRows / 2) + 1
		}
	],
	'dead': False,
	'deadReason': 'Razón desconocida',
	'isFirstPlayer': True
}

if Config.twoPlayersMode:
	snake['x'] = (Config.displayColumns / 2) - 1
	snake['tail'][0]['x'] = (Config.displayColumns / 2) - 1

snake2 = {
	'x': (Config.displayColumns / 2) + 1,
	'y': Config.displayRows / 2,
	'direction': False,
	'tail': [
		{
			'x': (Config.displayColumns / 2) + 1,
			'y': (Config.displayRows / 2) + 1
		}
	],
	'dead': False,
	'deadReason': 'Razón desconocida',
	'isFirstPlayer': False
}

generatedFood = {
	'x': -1,
	'y': -1
}

def control(key):
	if key[PG.K_w] and snake['direction'] != 'down':
		snake['direction'] = 'up'
	else:
		if key[PG.K_s] and snake['direction'] != 'up':
			snake['direction'] = 'down'
		else:
			if key[PG.K_a] and snake['direction'] != 'right':
				snake['direction'] = 'left'
			else:
				if key[PG.K_d] and snake['direction'] != 'left':
					snake['direction'] = 'right'

	if Config.twoPlayersMode:
		if key[PG.K_UP] and snake2['direction'] != 'down':
			snake2['direction'] = 'up'
		else:
			if key[PG.K_DOWN] and snake2['direction'] != 'up':
				snake2['direction'] = 'down'
			else:
				if key[PG.K_LEFT] and snake2['direction'] != 'right':
					snake2['direction'] = 'left'
				else:
					if key[PG.K_RIGHT] and snake2['direction'] != 'left':
						snake2['direction'] = 'right'

def setSnakePosition():
	if snake['direction']:
		for i in reversed(range(0, len(snake['tail']), 1)):
			if i <= 0:
				snake['tail'][i]['x'] = snake['x']
				snake['tail'][i]['y'] = snake['y']
			else:
				snake['tail'][i]['x'] = snake['tail'][i - 1]['x']
				snake['tail'][i]['y'] = snake['tail'][i - 1]['y']

		if snake['direction'] == 'up' and snake['y'] >= 0:
			snake['y'] -= 1
		else:
			if snake['direction'] == 'down' and snake['y'] <= Config.displayRows - 1:
				snake['y'] += 1
			else:
				if snake['direction'] == 'left' and snake['x'] >= 0:
					snake['x'] -= 1
				else:
					if snake['direction'] == 'right' and snake['x'] <= Config.displayRows - 1:
						snake['x'] += 1

	if snake2['direction']:
		for i in reversed(range(0, len(snake2['tail']), 1)):
			if i <= 0:
				snake2['tail'][i]['x'] = snake2['x']
				snake2['tail'][i]['y'] = snake2['y']
			else:
				snake2['tail'][i]['x'] = snake2['tail'][i - 1]['x']
				snake2['tail'][i]['y'] = snake2['tail'][i - 1]['y']

		if snake2['direction'] == 'up' and snake2['y'] >= 0:
			snake2['y'] -= 1
		else:
			if snake2['direction'] == 'down' and snake2['y'] <= Config.displayRows - 1:
				snake2['y'] += 1
			else:
				if snake2['direction'] == 'left' and snake2['x'] >= 0:
					snake2['x'] -= 1
				else:
					if snake2['direction'] == 'right' and snake2['x'] <= Config.displayRows - 1:
						snake2['x'] += 1

def generateFood():
	generatedFood['x'] = random.randrange(0, Config.displayColumns - 1)
	generatedFood['y'] = random.randrange(0, Config.displayRows - 1)

def collisionsDriver():
	if snake['x'] == generatedFood['x'] and snake['y'] == generatedFood['y']:
		generateFood()
		snake['tail'] += [
			{
				'x': snake['tail'][ len(snake['tail']) - 1 ]['x'],
				'y': snake['tail'][ len(snake['tail']) - 1 ]['y']
			}
		]

	if snake['y'] < 0 and snake['direction'] == 'up' or snake['y'] > Config.displayColumns - 1 and snake['direction'] == 'down' or snake['x'] < 0 and snake['direction'] == 'left' or snake['x'] > Config.displayColumns - 1 and snake['direction'] == 'right':
		snake['deadReason'] = 'Chocaste con el borde'
		snake['dead'] = True

	for tail in snake['tail']:
		if tail['x'] == snake['x'] and tail['y'] == snake['y']:
			snake['deadReason'] = 'Chocaste con tu cola'
			snake['dead'] = True

	if Config.twoPlayersMode:
		if snake2['x'] == generatedFood['x'] and snake2['y'] == generatedFood['y']:
			generateFood()
			snake2['tail'] += [
				{
					'x': snake2['tail'][ len(snake2['tail']) - 1 ]['x'],
					'y': snake2['tail'][ len(snake2['tail']) - 1 ]['y']
				}
			]

		if snake2['y'] < 0 and snake2['direction'] == 'up' or snake2['y'] > Config.displayColumns - 1 and snake2['direction'] == 'down' or snake2['x'] < 0 and snake2['direction'] == 'left' or snake2['x'] > Config.displayColumns - 1 and snake2['direction'] == 'right':
			snake2['deadReason'] = 'Chocaste con el borde'
			snake2['dead'] = True

		for tail in snake2['tail']:
			if tail['x'] == snake2['x'] and tail['y'] == snake2['y']:
				snake2['deadReason'] = 'Chocaste con tu cola'
				snake2['dead'] = True

def gameOver(window):
	reason = snake['deadReason']
	score = str(len(snake['tail']) - 1)

	if Config.twoPlayersMode:
		score = 'Verde: ' + score + ', Rojo: ' + str(len(snake2['tail']) - 1)

		if snake2['dead']:
			reason = 'Jugador rojo: ' + snake2['deadReason']
		else:
			reason = 'Jugador verde: ' + reason

	def title():
		textFont = PG.font.SysFont('Algerian', 40)
		text = textFont.render(score, False, (Color.lightGreen), (Config.windowFillColor))
		textRect = text.get_rect()
		textRect.centerx = window.get_rect().centerx
		textRect.centery = window.get_rect().centery
		window.blit(text, textRect)

	def subtitle():
		textFont = PG.font.SysFont('Verdana', 14)
		text = textFont.render(reason, False, (Color.lightGreen), (Config.windowFillColor))
		textRect = text.get_rect()
		textRect.centerx = window.get_rect().centerx
		textRect.centery = window.get_rect().centery + 50
		window.blit(text, textRect)

	def pressSpaceText():
		textFont = PG.font.SysFont('Verdana', 20)
		text = textFont.render('Presiona espacio para reiniciar', False, (Color.lightGreen), (Config.windowFillColor))
		textRect = text.get_rect()
		textRect.centerx = window.get_rect().centerx
		textRect.centery = window.get_rect().centery + 250
		window.blit(text, textRect)

	title()
	subtitle()
	pressSpaceText()

def main():
	PG.init()

	window = PG.display.set_mode(Config.windowSize)
	PG.display.set_caption(Config.windowTitle)

	run = True
	while run:
		PG.time.delay(Config.updateDelay)
		for event in PG.event.get():
			if event.type == PG.QUIT:
				run = False

			# For controls
			key = PG.key.get_pressed()

			if not snake['dead'] and not snake2['dead']:
				control(key)
			else:
				if key[PG.K_SPACE]:
					snake['direction'] = False
					snake['x'] = Config.displayColumns / 2
					snake['y'] = Config.displayRows / 2
					snake['tail'] = [
						{
							'x': Config.displayColumns / 2,
							'y': (Config.displayRows / 2) + 1
						}
					]
					snake['dead'] = False

					if Config.twoPlayersMode:
						snake['x'] = (Config.displayColumns / 2) - 1
						snake['tail'][0]['x'] = (Config.displayColumns / 2) - 1

						snake2['dead'] = False
						snake2['direction'] = False
						snake2['x'] = (Config.displayColumns / 2) + 1
						snake2['y'] = Config.displayRows / 2
						snake2['tail'] = [
							{
								'x': (Config.displayColumns / 2) + 1,
								'y': (Config.displayRows / 2) + 1
							}
						]

					generateFood()
		
		window.fill(Config.windowFillColor)

		if not snake['dead'] and not snake2['dead']:
			# Generate food if food position negative
			if generatedFood['x'] < 0 or generatedFood['y'] < 0:
				generateFood()

			# Draw
			setSnakePosition()
			if not Config.twoPlayersMode:
				Snake.draw(window, snake)
			else:
				if len(snake['tail']) > len(snake2['tail']):
					Snake.draw(window, snake2)
					Snake.draw(window, snake)
				else:
					Snake.draw(window, snake)
					Snake.draw(window, snake2)

			SnakeFood.draw(window, generatedFood)
			collisionsDriver()
		else:
			gameOver(window)
		
		PG.display.update()
	PG.quit()
main()