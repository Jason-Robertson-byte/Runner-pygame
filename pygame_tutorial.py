#introduction to py.game
import pygame
from sys import exit # used to exit python
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = test_font.render(f'Score:{current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:screen.blit(snail_surf,obstacle_rect)
            else: screen.blit(fly_surf,obstacle_rect)

            obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100] #deletes rectangles if they leave the screen

        return obstacle_list
    else: return [] #none does not have an append method; timer needs to start before list contains values

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1 #slowly increases the index so that switching images takes more time
        if player_index>=len(player_walk): player_index = 0


        player_surf = player_walk[int(player_index)]

pygame.init() # initializes pygame module. Must be called in all pygames.
screen = pygame.display.set_mode((800,400)) # sets window size (Display Surface - width, height)
pygame.display.set_caption('Runner') # sets name title of window
clock = pygame.time.Clock() #variable used to control the ceiling frame rate
test_font = pygame.font.Font('pygame tutorial\Pixeltype.ttf', 50) # argument (font type, font size)
game_active = False
start_time = 0
score = 0

sky_surface = pygame.image.load('pygame tutorial\Sky.png').convert() # "C:\Users\rober\mu_code\pygame tutorial\Sky.png"
ground_surface = pygame.image.load('pygame tutorial\ground.png').convert() # "C:\Users\rober\mu_code\pygame tutorial\ground.png"



#Snail
snail_frame1= pygame.image.load('pygame tutorial\snail1.png').convert_alpha()
snail_frame2 = pygame.image.load('pygame tutorial\snail2.png').convert_alpha()
snail_frames = [snail_frame1,snail_frame2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

#Fly
fly_frame1 = pygame.image.load('pygame tutorial\Fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('pygame tutorial\Fly2.png').convert_alpha()
fly_frames = [fly_frame1,fly_frame2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

player_walk_1 = pygame.image.load('pygame tutorial\player_walk_1.png').convert_alpha() #convert make image easier for python to process, alpha removes white space
player_walk_2 = pygame.image.load('pygame tutorial\player_walk_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load('pygame tutorial\jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom =(80,300))
player_gravity = 0

#Intro Screen
player_stand = pygame.image.load('pygame tutorial\player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2) # arguments (surface,angle,scale)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Pixel Runner',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400, 335))

#Timer
obstacle_timer = pygame.USEREVENT +1 #creates a custom user event (always add +1,2,3 etc. to avoid conflict with the black boxes of pygame module)
pygame.time.set_timer(obstacle_timer,1500) #arguments (trigger, time); controls speed of obstacles

snail_animation_timer = pygame.USEREVENT +2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT +3
pygame.time.set_timer(fly_animation_timer,200)





while True: #infinite loop used to display window and avoid it automatically closing; game runs inside loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #references the X button to close the window
            pygame.quit()
            exit() # exits python to avoid user seeing an error statement

        if game_active:
            if event.type ==pygame.KEYDOWN: #references pressing a key
                if event.key ==pygame.K_SPACE and player_rect.bottom >=300: #K_SPACE references the space bar
                    player_gravity = -20

            if event.type ==pygame.MOUSEBUTTONDOWN and player_rect.bottom >=300: #references clicking the mouse button
                if player_rect.collidepoint(event.pos): #defines the colide point to be the mouse point and the player rectangle
                    player_gravity = -20
        else:
            if event.type ==pygame.KEYDOWN and event.key ==pygame.K_SPACE:
                 game_active = True
                 start_time = int(pygame.time.get_ticks()/1000)

        if game_active:
            if event.type ==obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright =(randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright =(randint(900,1100),210)))

            if event.type ==snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type ==fly_animation_timer:
                if fly_frame_index ==0: fly_frame_index = 1
                else: fly_frame_index =0
                fly_surf = fly_frames[fly_frame_index]




    if game_active:
        screen.blit(sky_surface,(0,0)) #argument x,y are the coordinates the surface appear on the display surface - always starts from top left
        screen.blit(ground_surface,(0,300))

        score = display_score()

        #Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)


        #Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf,player_rect)

        #collision
        game_active = collisions(player_rect,obstacle_rect_list) #changes value to false if collision occurs via collisions function

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear() #needed to reset objects to default positions or will continue to have collisions
        player_rect.midbottom = (80,300) #resets player position
        player_gravity = 0 #resets player gravity
        screen.blit(game_name,game_name_rect)



        score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))
        if score == 0: screen.blit(game_message,game_message_rect)
        else: screen.blit(score_message,score_message_rect)


    pygame.display.update()
    clock.tick(60) # controls frame rate



#Additional Tutorial Notes:

#tutorial element (Replaced code)   test_surface = pygame.Surface((100,200))
#tutorial elememt (Replaced code)   test_surface.fill('Red') #fills surface with specified color - https://www.pygame.org/docs/ref/color_list.html


        #pygame.draw.rect(screen,'#c0e8ec' ,score_rect) #hexadecimal system used for color in this instance
        #pygame.draw.rect(screen,'#c0e8ec' ,score_rect,10) #when adding width, fill disappears so duplicate is needed for border
        #screen.blit(score_surf,score_rect)

#keys = pygame.key.get_pressed()
# if keys[pygame.K_SPACE]:

#if player_rect.colliderect(snail_rect):


#Alternates - Tutorial: pygame.mouse
#mouse_pos = pygame.mouse.get_pos()    #gets position of the mouse (x,y)
#if player_rect.collidepoint(mouse_pos):
    #print('collision')
    #print(pygame.mouse.get_pressed()) # returns boolean True if mouse buttons are pressed

#if event.type ==pygame.MOUSEMOTION -a means of getting mouse position; other Alternates include pygame.MOUSEBUTTONUP and pygame.MOUSEBUTTONDOWN
#                                           which return mouse up or mouse down for holding or releasing mouse button respectively

# pygame.draw.rect(screen,'Pink',score_rect,6,20) # arguements -surface, color, rectangle, width, border radius
#pygame.draw.ellipse(screen, 'Brown',pygame.Rect(Left,top,width,height))
#rgb_color = (red, green, blue) 0 - 255
#hex_color = #rrggbb 0 -ff

#player_stand = pygame.transform.scale(player_stand,(100,200)) #resize the image (image,width,height)
#player_stand = pygame.transform.scale2x(player_stand) #doubles image size

 #       snail_rect.x -= 4
 #       if snail_rect.right <=0:snail_rect.left = 800
 #       screen.blit(snail_surf,snail_rect,)
   #screen.blit(game_message,game_message_rect)
 #score_surf = test_font.render('My game', False, (64,64,64)) #argument (text, AA, color)
#score_rect = score_surf.get_rect(center =(400,50))
#snail_rect.left = 800 #resets snail position after a collision
#snail_rect = snail_surf.get_rect(bottomright =(600,300)) #creates a rectangle the size of the image surface; argument places rectangle
#                                                         based on defined point at x,y coordinates

#collision
#if snail_rect.colliderect(player_rect):
#game_active = False

#snail_surf = pygame.image.load('pygame tutorial\snail1.png').convert_alpha() #"C:\Users\rober\mu_code\pygame tutorial\snail1.png"
#fly_surf = pygame.image.load('pygame tutorial\Fly1.png').convert_alpha()
