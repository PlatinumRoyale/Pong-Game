#note this reqires the simplegui module which is available at www.codeskultor.com

import simplegui
import random

#important global variables
frame_width=700
frame_height=400
player1_score=0
player2_score=0

#Paddle global variables
paddle_width=10
paddle_height=100
paddle1_position=(frame_height/2)-(paddle_height/2)
paddle2_position=(frame_height/2)-(paddle_height/2)
paddle1_velocity=0
paddle2_velocity=0
paddle_velocity=8

#Ball global Variables
ball_radius=10
ball_position=[frame_width/2,frame_height/2]
ball_velocity=[1,1]
direction="right"

def game_draw(canvas):
    global player1_score,player2_score,paddle1_position,paddle2_position,paddle1_velocity,paddle2_velocity
    # draw Center Line
    canvas.draw_line([frame_width / 2, 0],[frame_width/ 2,frame_height],2, "White")
    
    # update ball
    ball_position[0] += ball_velocity[0]
    ball_position[1] += ball_velocity[1]
    
    #bottom or top collision detection
    if (ball_position[1] <= ball_radius or ball_position[1] >= frame_height -ball_radius):
        ball_velocity[1] = - ball_velocity[1]
    
    #gutter or paddle detection
    if (ball_position[0] <= ball_radius + paddle_width):
        if (ball_position[1]-ball_radius <= paddle1_position+paddle_height and ball_position[1]+ball_radius >= paddle1_position):
            ball_velocity[0] = -(ball_velocity[0] + 0.1*ball_velocity[0])
            ball_velocity[1] += 0.1*ball_velocity[1]
        else:            
            ball_direction("right")
            player1_score += 1
    if (ball_position[0] >= frame_width - paddle_width -ball_radius):
        if (ball_position[1]-ball_radius <= paddle2_position+paddle_height and ball_position[1]+ball_radius >= paddle2_position):
            ball_velocity[0] = -(ball_velocity[0] + 0.1*ball_velocity[0])
            ball_velocity[1] += 0.1*ball_velocity[1]
        else:
            ball_direction("left")
            player2_score += 1
    # draw ball
    canvas.draw_circle(ball_position,ball_radius, 5, "White", "White")
    
    
    #Confine paddels to screen space
    paddle1_position += paddle1_velocity
    paddle2_position += paddle2_velocity
    if (paddle1_position <= 0):
        paddle1_position = 0
    if (paddle1_position >=frame_height - paddle_height):
        paddle1_position = frame_height - paddle_height
    if (paddle2_position <= 0):
        paddle2_position = 0
    if (paddle2_position >= frame_height - paddle_height):
        paddle2_position = frame_height - paddle_height    
    
    #Draw paddle1                                                            
    canvas.draw_polygon([(0,paddle1_position),(paddle_width,paddle1_position),(paddle_width,paddle1_position+paddle_height),(0,paddle1_position+paddle_height)],2,"White","White")
    #Draw paddle2
    canvas.draw_polygon([(frame_width,paddle2_position),(frame_width-paddle_width,paddle2_position),(frame_width-paddle_width,paddle2_position+paddle_height),(frame_width,paddle2_position+paddle_height)],2,"White","White")
    #Draw Player 1 Score
    canvas.draw_text(str(player1_score),[frame_width/2+50,50], 48,"Pink")
    #Draw Player 2 Score
    canvas.draw_text(str(player2_score),[frame_width/2-50,50], 48,"Pink")
    
    
    if(player1_score>=10):
        message="Player 1 Wins!"
        ball_direction("stop")
        canvas.draw_polygon([(0,0),(frame_width,0),(frame_width,frame_height),(0,frame_height)],1,"Black","Black")
        canvas.draw_text(message,[(frame_width/2)-150,200], 48,"Yellow",'monospace')
    if(player2_score>=10):
        message="Player 2 Wins!"
        ball_direction("stop")
        canvas.draw_polygon([(0,0),(frame_width,0),(frame_width,frame_height),(0,frame_height)],1,"Black","Black")
        canvas.draw_text(message,[(frame_width/2)-150,200], 48,"Yellow",'monospace')
    
def keydown(key):
    global paddle1_velocity, paddle2_velocity, paddle_velocity, pause_state
    if key == simplegui.KEY_MAP["w"]:
        paddle1_velocity = -paddle_velocity
    if key == simplegui.KEY_MAP["s"] :
        paddle1_velocity = paddle_velocity
    if key == simplegui.KEY_MAP["down"]:
        paddle2_velocity = paddle_velocity
    if key == simplegui.KEY_MAP["up"]:
        paddle2_velocity = -paddle_velocity
        
def keyup(key):
    global paddle1_velocity, paddle2_velocity
    if key == simplegui.KEY_MAP["w"]:
        paddle1_velocity = 0
    if key == simplegui.KEY_MAP["s"]:
        paddle1_velocity = 0
    if key == simplegui.KEY_MAP["down"]:
        paddle2_velocity = 0
    if key == simplegui.KEY_MAP["up"]:
        paddle2_velocity = 0
        
def ball_direction(direction):
    global ball_position, ball_velocity 
    ball_position = [frame_width / 2, frame_height / 2]
    if direction == "right":
        ball_velocity = [random.randrange(120, 240)/60, -random.randrange(60, 180)/60]
    elif direction == "left":
        ball_velocity = [-random.randrange(120, 240)/60, -random.randrange(60, 180)/60]
    elif direction == "stop":
        ball_velocity = [0,0]
        
def newGame():
    reset()
    game_frame=simplegui.create_frame("PONG GAME",frame_width,frame_height)
    game_frame.add_button('BACK', back, 100)
    game_frame.add_button('RESET', reset, 100)
    game_frame.set_draw_handler(game_draw)
    game_frame.set_keydown_handler(keydown)
    game_frame.set_keyup_handler(keyup)
    game_frame.start();
def reset():
    global player1_score,player2_score,ball_velocity
    ball_velocity=[1,1]
    player1_score=0
    player2_score=0
    direct=["left","right"]
    direction=(random.choice(direct))
    ball_direction(direction)
def draw_help(canvas):
    global frame_width,frame_height
    help_title="HELP"
    controls1="Player 2 Controls: W-Paddle Up  S-Paddle Down"
    controls2="Player 1 Controls: Up Arrow-Paddle Up  Down Arrow-Paddle Down"
    obj_title="Objective:"
    objective="Bounce the ball using your paddle in the opponents zone to score points"
    canvas.draw_text(help_title, [(frame_width/2)-50,50], 48, "Yellow")
    canvas.draw_text(controls1,[25,frame_height/2],20,"White")
    canvas.draw_text(controls2,[25,frame_height/2+20],20,"White")
    canvas.draw_text(obj_title,[25,frame_height-125],30,"White")
    canvas.draw_text(objective,[25,frame_height-105],20,"White")    
def help():
    help_frame = simplegui.create_frame("HELP",frame_width,frame_height)
    help_frame.add_button('BACK', back, 100)
    help_frame.set_draw_handler(draw_help)
    help_frame.start()
    
def back():
    main_menu()
def draw_load(canvas):
    global image,frame_width,frame_height
    load_title="LOADING"
    box_width=280
    box_height=10
    bar_width=2
    bar_height=10
    canvas.draw_text(load_title, [(frame_width/2)-100,frame_height/2], 48, "White",'monospace')
def tick():
    global timer
    newGame()
    timer.stop()
#timer variable that waits for 3 seconds
timer = simplegui.create_timer(3000, tick)
def load():
    global frame_width,frame_height,timer
    load_frame = simplegui.create_frame("LOADING",frame_width,frame_height)
    load_frame.set_draw_handler(draw_load)
    load_frame.start()
    timer.start();
def draw_main(canvas):
    global frame_width,frame_height
    game_title="PONG"
    canvas.draw_text(game_title, [(frame_width/2)-75,200], 70, "White",'monospace')
      
#Main menu function
def main_menu(): 
    frame = simplegui.create_frame("MAIN MENU",frame_width,frame_height)
    frame.set_draw_handler(draw_main)
    frame.add_button('NEW GAME', load, 100)
    frame.add_button('HELP', help, 100)
    frame.start()
#call main menu at the beginning    
main_menu()