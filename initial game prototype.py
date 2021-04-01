import pygame, math, random

pygame.init()

width = 1280
height = 720
display = pygame.display.set_mode((width, height))

# Global variables

clock = pygame.time.Clock() # it's the framerate

# Colors

black = (0, 0, 0)
white = (255, 255, 255)

# this is outside the loop for testing

cx = random.randint(20, width - 20) # max width of a circle is 20; no matter what the res, there will not be targets outside the
cy = random.randint(20, height - 20) # window the player can see
width_of_circle = random.randint(14, 20) # where the width of circles is set

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()



    x = pygame.mouse.get_pos()[0] # pulls the x value from the get_pos
    y = pygame.mouse.get_pos()[1] 
    click = pygame.mouse.get_pressed() # returns booleans for each mousebutton, if true when called then button is being clicked

    

    sqx = (x - cx)**2
    sqy = (y - cy)**2

    if math.sqrt(sqx + sqy) < width_of_circle and click[0] == 1: # if the circle created outside the loop is clicked, then it creates a new circle, and covers the previous circle
        display.fill(black)
        cx = random.randint(20, width - 20)
        cy = random.randint(20, height - 20)
        width_of_circle = random.randint(14, 20)

    
    pygame.draw.circle(display, white, (cx, cy), width_of_circle)

    pygame.display.update()
    clock.tick(60)
    
    