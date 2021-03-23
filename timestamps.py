import pygame as pg
import json
# setting up pygame
pg.init()
pg.mixer.init()
pg.font.init()

screen = pg.display.set_mode([500,500])
running = True
playing = False
finished = False
font = pg.font.SysFont('Verdana', 30)


# loading project data
project = "Men I Trust - Found me"
# audio
pg.mixer.music.load(f"{project}/audio.mp3")
# loading lyrics into 2D array
lyrics = open(f"{project}/lyrics.txt", "r", encoding="utf-8").read().split("\n")
lyrics = [x.split(" ") for x in lyrics]
if lyrics[-1] != ['']: lyrics.append(['']) # last part fix
# creating parts (3D array) by splitting by empty lines
parts = []
part = []
for i in lyrics:
	if i != ['']:
		part.append(i)
	else:
		parts.append(part)
		part = []
# :)
lyrics = parts
data = []
for part in lyrics:
	data.append([])
	for line in part:
		data[-1].append([])
		for word in line:
			data[-1][-1].append(0)
# indexes of current stuff
current_part = 0
current_line = 0
current_word = 0

def show_text(txt):
	textsurface = font.render(txt, False, (200,200,200))
	screen.blit(textsurface, [0,0])

def get_word():
	return lyrics[current_part][current_line][current_word]

def save_data():
	json_data = {"data": data} #xddddddddddddd
	with open(f"{project}/data.json", "w") as f:
		json.dump(json_data, f)


while running:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
		if event.type == pg.MOUSEBUTTONDOWN:
			if playing:
				# saving timestamp
				time = pg.mixer.music.get_pos()
				data[current_part][current_line][current_word] = [get_word(), time]
				# next word
				if current_word < len(lyrics[current_part][current_line])-1:
					current_word += 1
				elif current_line < len(lyrics[current_part])-1:
					current_line += 1
					current_word = 0
				elif current_part < len(lyrics)-1:
					current_part += 1
					current_line = 0
					current_word = 0
				else:
					finished = True

			else:
				playing = True
				pg.mixer.music.play()

	# drawing stuff
	screen.fill((20,20,20))
	if playing and not finished:
		# displaying current word
		word = get_word()
		show_text(word)
	elif playing and finished:
		show_text("Finished!")
		save_data()
		exit()
	else:
		show_text("Click to start!")

	pg.display.flip()
pg.quit()