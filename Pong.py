# Implementation of classic arcade game Pong

import simpleguitk as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2
paddle1_vel = 0
paddle2_vel = 0
LEFT = False
RIGHT = True
ball_pos = [WIDTH / 2, HEIGHT / 2]
scoreleft = 0
scoreright = 0
paddle_acc = 2

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    # Random velocity generated. 
    global ball_pos, ball_vel
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    random_horiz_vel_x = (random.randrange(120, 240) / 60.0)
    random_vert_vel_y = (random.randrange(60, 80) / 60.0)
    
    if direction == True:
        ball_vel = [random_horiz_vel_x, - random_vert_vel_y]
    elif direction == False:
        ball_vel = [- random_horiz_vel_x, - random_vert_vel_y]
    
# define event handlers
def new_game():
    global paddle_acc, paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, scoreleft, scoreright 
    scoreleft = 0
    scoreright = 0
    paddle_acc = 2
    paddle1_vel = 0
    paddle2_vel = 0
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    direction = random.choice([LEFT, RIGHT])
    spawn_ball(direction)

def draw(canvas):
    global paddle_acc, scoreleft, scoreright, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "white", "white")
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos <= HALF_PAD_HEIGHT:
        paddle1_pos = HALF_PAD_HEIGHT
    elif paddle1_pos >= HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT
    
    if paddle2_pos <= HALF_PAD_HEIGHT:
        paddle2_pos = HALF_PAD_HEIGHT
    elif paddle2_pos >= HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT
        
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
                
    # draw paddles
    canvas.draw_line([1, paddle1_pos - HALF_PAD_HEIGHT],\
                     [1, paddle1_pos + HALF_PAD_HEIGHT], PAD_WIDTH, "white")
    canvas.draw_line([WIDTH - 1, paddle2_pos - HALF_PAD_HEIGHT ],\
                     [WIDTH - 1, paddle2_pos + HALF_PAD_HEIGHT], PAD_WIDTH, "white")
    
    # determine whether paddle and ball collide 
    if (ball_pos[0] - BALL_RADIUS <= HALF_PAD_WIDTH) and paddle1_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
        ball_vel[0] =  - ball_vel[0] * 1.1
        paddle_acc = paddle_acc * 1.1
    elif (ball_pos[0] + BALL_RADIUS) >= WIDTH - HALF_PAD_WIDTH and paddle2_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
        ball_vel[0] =  - ball_vel[0] * 1.1
        paddle_acc = paddle_acc * 1.1
    
    # determine whether balls collide with gutter
    if (ball_pos[0] <= PAD_WIDTH):
        scoreright += 1
        paddle_acc = 2
        spawn_ball(RIGHT)
    elif (ball_pos[0] >= WIDTH - PAD_WIDTH):
        scoreleft += 1
        paddle_acc = 2
        spawn_ball(LEFT)

    # determine whether balls collide with top and bottom walls
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
    # draw scores
    canvas.draw_text(str(scoreleft), [200, 100], 48, "white")
    canvas.draw_text(str(scoreright), [400, 100], 48, "white")
        
def keydown(key):
    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP["W"]:
        paddle1_vel -= paddle_acc 
    elif key == simplegui.KEY_MAP["S"]:
        paddle1_vel += paddle_acc 
    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= paddle_acc
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += paddle_acc 
    
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["W"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["S"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
        
def restart():
    # Button handler that calls new_game()
    new_game()
    

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("New Game", restart, 200)

# start frame
new_game()
frame.start()