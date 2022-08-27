#introduction to py.game
import pygame
from sys import exit # used to exit python

def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = test_font.render(f'Score:{current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

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

#score_surf = test_font.render('My game', False, (64,64,64)) #argument (text, AA, color)
#score_rect = score_surf.get_rect(center =(400,50))

snail_surf = pygame.image.load('pygame tutorial\snail1.png').convert_alpha() #"C:\Users\rober\mu_code\pygame tutorial\snail1.png"
snail_rect = snail_surf.get_rect(bottomright =(600,300)) #creates a rectangle the size of the image surface; argument places rectangle
#                                                         based on defined point at x,y coordinates


player_surf = pygame.image.load('pygame tutorial\player_walk_1.png').convert_alpha() #convert make image easier for python to process, alpha removes white space
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
                 snail_rect.left = 800 #resets snail position after a collision
                 start_time = int(pygame.time.get_ticks()/1000)

    if game_active:
        screen.blit(sky_surface,(0,0)) #argument x,y are the coordinates the surface appear on the display surface - always starts from top left
        screen.blit(ground_surface,(0,300))

        score = display_score()

        snail_rect.x -= 4
        if snail_rect.right <=0:snail_rect.left = 800
        screen.blit(snail_surf,snail_rect,)

        #Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        screen.blit(player_surf,player_rect)

        #collision
        if snail_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name,game_name_rect)
        #screen.blit(game_message,game_message_rect)

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
