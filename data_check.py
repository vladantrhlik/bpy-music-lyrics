import time
import json
import pygame as pg

project = "Men I Trust - Found me"

pg.mixer.init()
pg.mixer.music.load(f"{project}/audio.mp3")
pg.mixer.music.play()

with open(f"{project}/data.json") as f:
  data = json.load(f)["data"]

# simplifying data to 2D array
words = []
for part in data:
	for line in part:
		for word in line:
			words.append(word)
pos = 0
while True:
	time = pg.mixer.music.get_pos()
	if abs(time - words[pos][1]) < 20:
		print(words[pos][0])
		pos += 1
