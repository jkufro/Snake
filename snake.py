#snake game
#use the arrow keys to change the snake's direction

import random
import sys
import tkinter
import time
from time import sleep

square_width = 20 #pixels
num_squares = 13 #changing this will change the size of the playable boardspace
score_bar_height = 48 #pixels
window_height = num_squares*square_width +score_bar_height
window_width = num_squares*square_width
game_speed_factor = 1.25 #lower makes the game faster

"""      %%%%%%%%%%%      MODEL      %%%%%%%%%%%%       """
def new_snake(): #starts a new snake 
	return [[random.randint(0,num_squares-1),random.randint(0,num_squares-1)]]

def check_edge(snake): #checks if the snake tries to move off of the board
	x = 0 <= snake[0][0] < num_squares
	y = 0 <= snake[0][1] < num_squares
	if x and y:
		return False
	return True

def check_eat_self(snake): #check to see if the snake tries to eat itself
	if snake[0] in snake[1:]:
		return True

def is_end_game(snake): 
	if check_eat_self(snake) or check_edge(snake):
		return True
	return False

def is_eating(): #handles if the snake is eating and the snake movement
	global food,score,snake
	next_move = [[snake[0][0]+direction[0],snake[0][1]+direction[1]]]
	if next_move[0] == food:
		score += 100
		snake = [[food[0],food[1]]] + snake
		food = new_food(snake)
	elif direction != [0,0]:
		snake = next_move + snake[:-1]

"""------------%%%%%%%%%%%%------------VIEW------------%%%%%%%%%%%%------------"""
def draw_board(snake,food,score,highscore): 
	c.delete(tkinter.ALL)
	c.create_rectangle(0,0,window_width,window_height,fill='black')
	draw_snake(snake)
	draw_food(food)
	c.create_rectangle(0,score_bar_height-2,window_width,score_bar_height,fill='white') #separation between board and score area
	draw_high_score(highscore)
	draw_score(score)
	window.update()

#helping functions for draw board
def draw_snake(snake):
	for box in snake:
		posx = box[0] * square_width
		posy = box[1] * square_width + score_bar_height
		c.create_rectangle(posx,posy,posx+square_width,posy+square_width,fill='white')

def draw_food(food):
	posx = food[0] * square_width
	posy = food[1] * square_width + score_bar_height
	c.create_rectangle(posx,posy,posx+square_width,posy+square_width,fill='red')

def draw_high_score(highscore):
	string = "HIGHSCORE:  " + highscore[0]
	c.create_text(score_bar_height//4,score_bar_height//2,anchor = "w",
		text = string,fill = 'white',font = ('Ubuntu',10))

def draw_score(score):
	string = "SCORE:  " + str(score)
	c.create_text(window_width-25,score_bar_height//2,anchor = "e",
		text = string,fill = 'white',font = ('Ubuntu',10))

def game_over_show(score):
	c.delete(tkinter.ALL)
	c.create_rectangle(0,0,window_width,window_height,fill='black')
	c.create_rectangle(0,score_bar_height-2,window_width,score_bar_height,fill='white')
	draw_snake(snake)
	draw_food(food)
	draw_high_score(highscore)
	draw_score(score)
	c.create_text(window_width//2,window_height//1.5, anchor = "s",
		text = "GAME\nOVER\n",fill = 'gray',font = ('Ubuntu',25))

	c.create_text(window_width//2,window_height//1.5+30, anchor = "s",
		text = "score: "+str(score),fill = 'gray',font = ('Ubuntu',25))

	window.update()

def win_show(score):
	c.delete(tkinter.ALL)
	c.create_rectangle(0,0,window_width,window_height,fill='black')
	c.create_rectangle(0,score_bar_height-2,window_width,score_bar_height,fill='white')
	draw_snake(snake)
	draw_food(food)
	draw_high_score(highscore)
	draw_score(score)
	c.create_text(window_width//2,window_height//1.5, anchor = "s",
		text = "YOU\nWIN\n",fill = 'gray',font = ('Ubuntu',25))

	c.create_text(window_width//2,window_height//1.5+30, anchor = "s",
		text = "score: "+str(score),fill = 'gray',font = ('Ubuntu',25))

	window.update()

"""------------%%%%%%%%%%%%------------CONTROLLER------------%%%%%%%%%%%%------------"""
def new_food(snake):
	pos = [random.randint(0,num_squares-1),random.randint(0,num_squares-1)]
	while pos in snake:
		pos = [random.randint(0,num_squares-1),random.randint(0,num_squares-1)]
	return pos

def retrieve_high_score():
    highscore = []
    with open("highscore.txt") as file:
        for line in file:
            highscore.append(line)
    for index in range(1): #remove the newline character
        data = list(highscore[index])
        del data[-1]
        highscore[index] = ''.join(data)
    return highscore

def update_high_score(score,name):
    file = open("highscore.txt","w")
    text = str(score)+"\n"
    file.write(text)


#------------------------------------------------------------------------------------------------------#

#game is a specified number of squares with side length 20px and a score bar at the top with height 50px
window = tkinter.Tk()

#key events 
""" direction is [0,-1] up     [1,0] right     [-1,0] left      [0,1] down"""
def left_arrow(event):
	global direction,frame_direction
	if frame_direction == [1,0]:
		return None
	direction = [-1,0]
def right_arrow(event):
	global direction,frame_direction
	if frame_direction == [-1,0]:
		return None
	direction = [1,0]
def up_arrow(event):
	global direction,frame_direction
	if frame_direction == [0,1]:
		return None
	direction = [0,-1]
def down_arrow(event):
	global direction,frame_direction
	if frame_direction == [0,-1]:
		return None
	direction = [0,1]

window.bind('<Left>',left_arrow)
window.bind('<Right>',right_arrow)
window.bind('<Up>',up_arrow)
window.bind('<Down>',down_arrow)


c = tkinter.Canvas(window,height = num_squares*square_width+score_bar_height, width = num_squares*square_width)
c.pack()

frame_direction = [0,0] #using this prevents the player from being able to turn 180 degrees in to themself


#game loop
while True:
	win = False #used for logic on displaying the correct end screen
	starting = True #used to prevent direction changes between games
	highscore = retrieve_high_score()
	score = 0
	snake = new_snake()
	food = new_food(snake)
	direction = [0,0]
	current_time = time.time() #used in when updating the board
	while not is_end_game(snake):
		draw_board(snake,food,score,highscore)
		this_time = time.time()-current_time
		if starting == True:
			direction = [0,0]
		if this_time > .1125*game_speed_factor: #update board after specific time has passed
			frame_direction = direction
			is_eating()
			current_time = time.time()
			if starting == True:
				direction = [0,0]
				starting = False
		if len(snake) >= num_squares**2:
			win_show(score)
			win = True
			break
	if score > int(highscore[0]):
		update_high_score(score,"")
	if win == False:
		game_over_show(score)
	while this_time < 3:
		this_time = time.time()-current_time


