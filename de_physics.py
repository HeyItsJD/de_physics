import pygame
from gpiozero import LED

# 4 is bomb

led = LED(4)
led.off()

# Initialize mixer
pygame.init()
pygame.display.init()
pygame.mixer.init()

# Define custom events (Timers Lmao)
TEXTDOWN = pygame.USEREVENT + 1
BEEPINTERVAL = pygame.USEREVENT + 2
CLEARTEXT = pygame.USEREVENT + 3
CLOSE = pygame.USEREVENT + 4

screen = pygame.display.set_mode((250, 250))
clock = pygame.time.Clock() # this is practially the update function

# Sound Bullshit
type_sound = pygame.mixer.Sound('click.mp3')
start_sound = pygame.mixer.Sound('start.mp3')
planting_sound = pygame.mixer.Sound('planted.mp3')
beep = pygame.mixer.Sound('beep.mp3')
boom = pygame.mixer.Sound('boom.mp3')
font = pygame.font.SysFont(None, 50) # Font size
text = ""  # Input text
input_active = True
countdown_time = 40
max_interval = 2100 # this is in milliseconds, so 2.1 seconds 
min_interval = 50  # same here its 0.05 seconds
exponential_decay = 0.95 # dont touch this or i will fucking kill you
time_left = countdown_time # uhhhh copied and pasted from stack overflow, i have no idea what this does but it works so im not gonna question it
current_interval = max_interval # ints the interval between beeps at max
last_tick = pygame.time.get_ticks() 

pygame.display.set_caption("de_physics Bomb Timer")

start_sound.play()

code = 1 # 7355608 actual bomb code but for debugging it 1
run = True # this means pygame is running once this is false shit will stop working yayayaya

while run:
    clock.tick(60) # 60fps
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            input_active = True
            text = ""
        elif event.type == pygame.KEYDOWN and input_active:
            type_sound.play()
            if event.key == pygame.K_RETURN:
                if int(text) == code:
                    input_active = False
                    planting_sound.play()
                    beep.play()
                    pygame.time.set_timer(TEXTDOWN, 1000)
                    pygame.time.set_timer(BEEPINTERVAL, int(current_interval))
                    text = str(countdown_time)
                    led.on()
                elif int(text) != code:
                    text = "Incorrect!"
                    pygame.time.set_timer(CLEARTEXT, 1000)
            elif event.key == pygame.K_BACKSPACE: # removes text
                text =  text[:-1]
            elif event.unicode.isdigit(): #adds a digit only not a str
                text += event.unicode
        elif event.type == TEXTDOWN: 
            countdown_time -= 1
            text = str(countdown_time)
            if countdown_time < 0:
                countdown_time = 0
                
                boom.play()
                text = "Boom!"
                pygame.time.set_timer(BEEPINTERVAL, 0)
                pygame.time.set_timer(TEXTDOWN, 0)
                pygame.time.set_timer(CLOSE, 2000)
        elif event.type == BEEPINTERVAL:
            current_interval = max(min_interval, int(current_interval * exponential_decay))
            pygame.time.set_timer(BEEPINTERVAL, int(current_interval))
            beep.play()
            led.blink(on_time=0.1, off_time=0.1, n=1) # blinks the led once every beep
        elif event.type == CLEARTEXT:
            text = ""
            pygame.time.set_timer(CLEARTEXT, 0)
        elif event.type == CLOSE:
            run = False
            pygame.time.set_timer(CLOSE, 0)
        screen.fill(0)
        text_surf = font.render(text, True, (255, 0, 0))
        screen.blit(text_surf, text_surf.get_rect(center = screen.get_rect().center))
        pygame.display.flip()
pygame.quit()
exit()



t = 40

countdown(int(t))