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
DARK_RED = (195, 0, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 195, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (220, 220, 0)
ORANGE = (255, 165, 0)

FONT = pygame.font.Font('freesansbold.ttf', 32)
SCORE_FONT = pygame.font.Font(None, 28)
game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Typewriter")
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
star_img = pygame.image.load('./resources/star.png')
num_lives = 5

# functions
def display_lives():
	global num_lives
	x = 1000
	y = 50

	for i in range(num_lives, 0, -1):
		game_display.blit(star_img, (x, y))
		x -= 35

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

def display_start_menu():
	MENU_FONT = pygame.font.Font("freesansbold.ttf", 28)
	TILE_TEXT_FONT = pygame.font.Font('freesansbold.ttf', 70)
	title_text = TILE_TEXT_FONT.render("Typewriter", True, WHITE, BLACK)
	title_text_rect = title_text.get_rect()
	title_text_rect.center = ((DISPLAY_WIDTH/2), (DISPLAY_HEIGHT/4))
	menu = True

	while menu:
		# check for exiting game early
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		game_display.fill(BLACK)
		game_display.blit(title_text, title_text_rect)

		# get mouse x and y
		mouse_x = pygame.mouse.get_pos()[0]
		mouse_y = pygame.mouse.get_pos()[1]

		# get left mouse clicked val
		clicked = pygame.mouse.get_pressed()[0]

		# easy mode button settings
		easy_button_length = 100
		easy_button_width = 30
		easy_button_x = DISPLAY_WIDTH/2 - easy_button_length/2
		easy_button_y = DISPLAY_HEIGHT/2

		# hard mode button settings
		hard_button_length = 100
		hard_button_width = 30
		hard_button_x = DISPLAY_WIDTH/2 - hard_button_length/2
		hard_button_y = DISPLAY_HEIGHT/2 + 3*hard_button_width

		# button container panel settings
		button_container_length = 200
		button_container_width = 6*easy_button_width
		button_container_x = DISPLAY_WIDTH/2 - button_container_length/2
		button_container_y = DISPLAY_HEIGHT/2 - easy_button_width

		# draw button container
		pygame.draw.rect(game_display, BLUE, (button_container_x, button_container_y, button_container_length, button_container_width))

		# easy button highlighting functionality
		if easy_button_x + easy_button_length > mouse_x > easy_button_x and easy_button_y + easy_button_width > mouse_y > easy_button_y:
			pygame.draw.rect(game_display, GREEN, (easy_button_x, easy_button_y, easy_button_length, easy_button_width))
			if clicked:
				return "Easy"

		else:
			pygame.draw.rect(game_display, DARK_GREEN, (easy_button_x, easy_button_y, easy_button_length, easy_button_width))

		# hard button highlighting functionality 
		if hard_button_x + hard_button_length > mouse_x > hard_button_x and hard_button_y + hard_button_width > mouse_y > hard_button_y:
			pygame.draw.rect(game_display, RED, (hard_button_x, hard_button_y, hard_button_length, hard_button_width))
			if clicked:
				return "Hard"
		else:
			pygame.draw.rect(game_display, DARK_RED, (hard_button_x, hard_button_y, hard_button_length, hard_button_width))
		
		# button texts
		easy_text = MENU_FONT.render("Easy", True, BLACK)
		easy_text_rect = easy_text.get_rect()
		easy_text_rect.x = easy_button_x + easy_button_length/5
		easy_text_rect.y = easy_button_y
		
		hard_text = MENU_FONT.render("Hard", True, BLACK)
		hard_text_rect = hard_text.get_rect()
		hard_text_rect.x = hard_button_x + hard_button_length/5
		hard_text_rect.y = hard_button_y

		game_display.blit(easy_text, easy_text_rect)
		game_display.blit(hard_text, hard_text_rect) 

		pygame.display.update()
		clock.tick(15)


def pause():
	PAUSE_FONT = pygame.font.Font("freesansbold.ttf", 35)
	pause_text = PAUSE_FONT.render("Paused", True, WHITE, BLACK)
	pause_rect = pause_text.get_rect()
	pause_rect.center = (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2)
	paused = True

	game_display.blit(pause_text, pause_rect)
	pygame.display.update()


	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					return True

		clock.tick(5)



# display start menu and set difficulty for game
difficulty = display_start_menu()

if difficulty == "Easy":
	file_name = "./resources/small_dictionary.txt"
else:
	file_name = "./resources/dictionary.txt"

#Game Loop

# words is current list of all words on screen
words = []

# dictionary is all words to choose from to add to words on screen, read from dictionary.txt
dictionary = []

with open(file_name, 'r') as f:
	for line in f:
		dictionary.append(line.rstrip())

dict_len = len(dictionary)
running = True
game_over = False

while running:
	if game_over:
		game_over_text = FONT.render("Game Over", True, WHITE, BLACK)
		game_over_rect = game_over_text.get_rect()
		game_over_rect.x = DISPLAY_WIDTH / 2 - (game_over_rect.right - game_over_rect.left) / 2
		game_over_rect.y = DISPLAY_HEIGHT / 2
		game_display.blit(game_over_text, game_over_rect)
		pygame.display.update()

	while game_over:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				game_over = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					running = False
					game_over = False
					
	#Process input (events)
	for event in pygame.event.get():
		#check for closing window
		if event.type == pygame.QUIT:
			running = False

		# check for typing a letter
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_1:
				running = pause()
			elif event.key == pygame.K_BACKSPACE:
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
			num_lives -= 1

			# game ends after missing 5 words
			if num_lives <= 0:
				game_over = True			

		elif word.is_typed():
			words.remove(word)
			current_typed_chars = ""
			score += len(word.get_word()) + math.ceil(speed_up_factor) 

	#Draw/Render
	game_display.fill(BLACK)
	display_typed_chars()
	display_score()
	display_lives()

	for word in words:
		word.draw(game_display)

	pygame.display.update()
	dt = clock.tick(FPS)
	time_since_last_added_word += dt

	# check if we should add another word to the screen because either all words have been typed or 4 seconds has passed
	# note: empty lists (and strings and tuples) are false, so check if not words to check if words is empty
	if not words or time_since_last_added_word > new_word_timer:
		words.append(WordBox(-300, random.randint(60, DISPLAY_HEIGHT-50), dictionary[random.randint(0, dict_len-1)]))
		time_since_last_added_word = 0
		speed_up_factor += 0.05
		new_word_timer -= 100 

		# words never move faster than 6 pixels
		if speed_up_factor > 4:
			speed_up_factor = 4

		# time between words never smaller than 1500 milliseconds
		if new_word_timer < 1500:
			new_word_timer = 1500

pygame.quit()