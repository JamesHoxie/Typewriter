import pygame
import random

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

FONT = pygame.font.Font('freesansbold.ttf', 32)
game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Typing Game")
clock = pygame.time.Clock()
time_since_last_added_word = 0
current_typed_chars = ""



# word box class
class WordBox():
	def __init__(self, x, y, word):
		# set word for this word box to display
		self.word = word
		self.x = x
		self.y = y
		self.text = FONT.render(self.word, True, GREEN, BLUE)
		self.textRect = self.text.get_rect()
		self.textRect.center = (self.x, self.y)
		self.typed = False
	
	def update(self):
		global current_typed_chars
		# advance word box to right with each call to update, highlight typed letters of this word, flag word to be removed if whole word is typed
		self.x += 2
		self.textRect.center = (self.x, self.y)

		# if word has been typed, set self.typed = True
		if current_typed_chars == self.word:
			self.typed = True
			current_typed_chars = ""

	def draw(self, game_display):
		game_display.blit(self.text, self.textRect)

	def is_typed(self):
		return self.typed == True

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
		if word.is_typed() or word.x > DISPLAY_WIDTH:
			words.remove(word)
	
	print(current_typed_chars)

	#Draw/Render
	game_display.fill(BLACK)
	
	for word in words:
		word.draw(game_display)

	pygame.display.update()
	dt = clock.tick(FPS)
	time_since_last_added_word += dt

	# check if we should add another word to the screen because either all words have been typed or 4 seconds has passed
	# note: empty lists (and strings and tuples) are false, so check if not words to check if words is empty
	if not words or time_since_last_added_word > 4000:
		words.append(WordBox(-300, random.randint(0, DISPLAY_HEIGHT), dictionary[random.randint(0, dict_len-1)]))
		time_since_last_added_word = 0

pygame.quit()
