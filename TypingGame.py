import pygame
import random
import math

pygame.init()
#mixer handles sound
pygame.mixer.init()

DISPLAY_WIDTH = 1080
DISPLAY_HEIGHT = 480
FPS = 30


#palette
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (220, 220, 0)
ORANGE = (255, 165, 0)

FONT = pygame.font.Font('freesansbold.ttf', 32)
SCORE_FONT = pygame.font.Font(None, 28)
game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Typing Game")
clock = pygame.time.Clock()
time_since_last_added_word = 0
current_typed_chars = ""
typed_text = FONT.render(current_typed_chars, True, WHITE, BLACK)
typed_rect = typed_text.get_rect()
# words scroll across screen at 2 pixels per second, but will speed up by 0.1 pixels every time a new word is added
speed_up_factor = 0.0
# create a new word every 4 seconds to start, but with each new word, reduce timer
new_word_timer = 4000
score = 0
score_text = SCORE_FONT.render(str(score), True, WHITE, BLACK)
score_rect = score_text.get_rect()

# functions
def display_score():
	font_color = WHITE

	if score < 0:
		font_color = RED

	score_text = SCORE_FONT.render("Score: " + str(score), True, font_color, BLACK)
	score_rect = score_text.get_rect()
	score_rect.x = 930
	score_rect.y = 10
	game_display.blit(score_text, score_rect)

def display_typed_chars():
	typed_text = FONT.render(current_typed_chars, True, WHITE, ORANGE)
	typed_rect = typed_text.get_rect()
	typed_rect.x = 400
	typed_rect.y = 10
	game_display.blit(typed_text, typed_rect)

# classes
class WordBox():
	def __init__(self, x, y, word):
		# set word for this word box to display
		self.word = word
		self.word_len = len(word)
		self.typed_word = ""
		self.x = x
		self.y = y
		self.typed_text = FONT.render(self.typed_word, True, YELLOW, BLUE)
		self.text = FONT.render(self.word, True, GREEN, BLUE)
		self.text_rect = self.text.get_rect()
		self.typed_text_rect = self.typed_text.get_rect()
		self.text_rect.x = self.x
		self.text_rect.y = self.y
		self.typed_text_rect.x = self.x
		self.typed_text_rect.y = self.y
		self.typed = False
	
	def update(self):
		global current_typed_chars
		# advance word box to right with each call to update, highlight typed letters of this word, flag word to be removed if whole word is typed
		self.x += 2 + speed_up_factor
		self.text_rect.x = self.x
		self.typed_text_rect.x = self.x

		self.typed_word = ""

		# check how much of word has been typed
		for i in range(0, self.word_len):
			for j in range(i, len(current_typed_chars)):
				if self.word[i] != current_typed_chars[j]:
					break
				else:
					self.typed_word += current_typed_chars[j]
					break

		# if word has been typed, set self.typed = True
		if current_typed_chars == self.word:
			self.typed = True

		# update typed_text to be rendered to screen as highlighted text
		self.typed_text = FONT.render(self.typed_word, True, YELLOW, BLUE)

	def draw(self, game_display):
		game_display.blit(self.text, self.text_rect)
		game_display.blit(self.typed_text, self.typed_text_rect)

	def is_typed(self):
		return self.typed == True

	def get_x(self):
		return self.x

	def get_word(self):
		return self.word

	def get_typed_len(self):
		return len(self.typed_word)

#Game Loop

# words is current list of all words on screen
words = []

# words.append(WordBox(25, 25, "banana"))

# dictionary is all words to choose from to add to words on screen, read from dictionary.txt
dictionary = []

with open('dictionary.txt', 'r') as f:
	for line in f:
		dictionary.append(line.rstrip())

dict_len = len(dictionary)
running = True
while running:
	#Process input (events)
	for event in pygame.event.get():
		#check for closing window
		if event.type == pygame.QUIT:
			running = False

		# check for typing a letter
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_BACKSPACE:
				if len(current_typed_chars) > 0:
					current_typed_chars = current_typed_chars[:len(current_typed_chars)-1]
			else:
				current_typed_chars += event.unicode

	#Update
	for word in words:
		word.update()	

	# Remove typed words from words and words that passed the edge of the screen
	for word in words:
		if word.get_x() > DISPLAY_WIDTH:
			words.remove(word)
			# only clear typed chars if word that passed edge of screen was in process of being typed
			if word.get_typed_len() > 0:
				current_typed_chars = ""
			score -= len(word.get_word())
			

		elif word.is_typed():
			words.remove(word)
			current_typed_chars = ""
			score += len(word.get_word()) + math.ceil(speed_up_factor) 

	#Draw/Render
	game_display.fill(BLACK)
	display_typed_chars()
	display_score()

	for word in words:
		word.draw(game_display)

	pygame.display.update()
	dt = clock.tick(FPS)
	time_since_last_added_word += dt

	# check if we should add another word to the screen because either all words have been typed or 4 seconds has passed
	# note: empty lists (and strings and tuples) are false, so check if not words to check if words is empty
	if not words or time_since_last_added_word > new_word_timer:
		words.append(WordBox(-300, random.randint(15, DISPLAY_HEIGHT-50), dictionary[random.randint(0, dict_len-1)]))
		time_since_last_added_word = 0
		speed_up_factor += 0.05
		new_word_timer -= 100 

		# words never move faster than 6 pixels
		if speed_up_factor > 4:
			speed_up_factor = 4

		# time between words never smaller than 1500 milliseconds
		if new_word_timer < 1500:
			new_word_timer = 1500



		print(speed_up_factor)

pygame.quit()
