from lcdlib import LCD
import machine
import random
import utime

#declaring all RGB LED pins and button pins
red1 = machine.Pin(2, machine.Pin.OUT)
green1 = machine.Pin(3, machine.Pin.OUT)
blue1 = machine.Pin(4, machine.Pin.OUT)
button1 = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)

red2 = machine.Pin(6, machine.Pin.OUT)
green2 = machine.Pin(7, machine.Pin.OUT)
blue2 = machine.Pin(8, machine.Pin.OUT)
button2 = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)

red3 = machine.Pin(10, machine.Pin.OUT)
green3 = machine.Pin(11, machine.Pin.OUT)
blue3 = machine.Pin(12, machine.Pin.OUT)
button3 = machine.Pin(9, machine.Pin.IN, machine.Pin.PULL_UP)

red4 = machine.Pin(14, machine.Pin.OUT)
green4 = machine.Pin(15, machine.Pin.OUT)
blue4 = machine.Pin(22, machine.Pin.OUT)
button4 = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)


#turning off all LEDs
LEDs = [red1,green1,blue1,red2,green2,blue2,red3,green3,blue3,red4,green4,blue4]
for LED in Leds:
    LED.value(0)
#init LCD object
lcd=LCD(16,17,18,19,20,21)

#function to check the state of buttons
def checkbuttonstates():
    global buttonState1
    global prev_buttonState1
    global buttonState2
    global prev_buttonState2
    global buttonState3
    global prev_buttonState3
    global buttonState4
    global prev_buttonState4
#setting prev states
    prev_buttonState1 = buttonState1
    prev_buttonState2 = buttonState2
    prev_buttonState3 = buttonState3
    prev_buttonState4 = buttonState4
#setting current states
    buttonState1 = button1.value()
    buttonState2 = button2.value()
    buttonState3 = button3.value()
    buttonState4 = button4.value()
#simple score updating function
def scoreUpdate():
    global score
    score += 1
    lcd.clearLCD()
    lcd.display(f'score: {score}')
#function used to ensure button can't click multiple times for each press
def debounce(pin):
    state = pin.value()
    utime.sleep_ms(10)
    return pin.value() == state

#prompts for tutorial function
def tutorialprompt(prompt):
    prompts=['to advance pressthe right button','Good Job!','to play, an LED will light up','in front of a   button', 'you must press  the button', 'with the lit LED', 'as fast as      possible', 'the game will   become more', 'difficult over  time', 'Are you ready?' ]
    for words in prompts:
        if words == prompts[prompt]:
            return words

#the game's tutorial
def tutorial():
    
    promptnum = 0
    
    lcd.clearLCD()
    lcd.display(tutorialprompt(promptnum))
    while True:
        checkbuttonstates() 
    #code to check which button is being pressed to decide if it will move forward or back
        if debounce(button4) and buttonState4 == 0 and prev_buttonState4 == 1:
            try:
                lcd.clearLCD()
                promptnum += 1
                lcd.display(tutorialprompt(promptnum))
            except IndexError:
                break
            
        if debounce(button1) and buttonState1 == 0 and prev_buttonState1 == 1:
            if promptnum > 0:
                lcd.clearLCD()
                promptnum -= 1
                lcd.display(tutorialprompt(promptnum))
                
#the game loop
def game():
    global score
    global time_limit
    global rgb_leds
    score = -1
    scoreUpdate()
    time_limit = 2000
    prevled = None
    while True:
        #set a list of tuples containing rgb led pins, then select a random one
        rgb_leds = [(red1, green1, blue1), (red2, green2, blue2), (red3, green3, blue3), (red4, green4, blue4)]
        random_rgb_led = random.choice(rgb_leds)
        while random_rgb_led == prevled:
            random_rgb_led = random.choice(rgb_leds)
        #turn off all LEDs and randomly delay before lighting random LED
        for pin in rgb_leds:
            for led in pin:
                led.value(0)

        delay_time = random.randint(10, 700)
        utime.sleep_ms(delay_time)

        for pin in random_rgb_led:
            pin.value(1)

        start_time = utime.ticks_ms()
        button_pressed = False
        #check if correct button is pressed (GPT used here)
        while utime.ticks_diff(utime.ticks_ms(), start_time) < time_limit:
            checkbuttonstates()
            if debounce(button1) and buttonState1 == 0 and prev_buttonState1 == 1:
                if random_rgb_led == (red1, green1, blue1):
                    scoreUpdate()
                    button_pressed = True
                    break
                else:
                    handle_game_over()
                    break
            elif debounce(button2) and buttonState2 == 0 and prev_buttonState2 == 1:
                if random_rgb_led == (red2, green2, blue2):
                    scoreUpdate()
                    button_pressed = True
                    break
                else:
                    handle_game_over()
                    break
            elif debounce(button3) and buttonState3 == 0 and prev_buttonState3 == 1:
                if random_rgb_led == (red3, green3, blue3):
                    scoreUpdate()
                    button_pressed = True
                    break
                else:
                    handle_game_over()
                    break
            elif debounce(button4) and buttonState4 == 0 and prev_buttonState4 == 1:
                if random_rgb_led == (red4, green4, blue4):
                    scoreUpdate()
                    button_pressed = True
                    break
                else:
                    handle_game_over()
                    break
        #end game if button isn't pressed
        if not button_pressed:
            handle_game_over()
            break

        update_time_limit()


        prevled = random_rgb_led
#function for game loss
def handle_game_over():
    #turn off all LEDs, tell user the score, then allow them to replay
    for pin in rgb_leds:
        for led in pin:
            led.value(0)
    lcd.clearLCD()
    lcd.display(f'You Lose! Your  score was {score}')
    
    while True:
        checkbuttonstates()
        
        if debounce(button4) and buttonState4 == 0 and prev_buttonState4 == 1:
            lcd.clearLCD()
            lcd.display('Would you like  to play again?')
            
            while True:
                checkbuttonstates()
                
                if debounce(button4) and buttonState4 == 0 and prev_buttonState4 == 1:
                    game()
                    break
                

#update the time limit for the game function
def update_time_limit():
    global time_limit
    if score % 3 == 0:
        time_limit -= 100
        if time_limit < 400:
            time_limit = 400
#set all button states to be initially 0
buttonState1 = 0
prev_buttonState1 = 1
buttonState2 = 0
prev_buttonState2 = 1
buttonState3 = 0
prev_buttonState3 = 1
buttonState4 = 0
prev_buttonState4 = 1
#begin tutorial
lcd.clearLCD()
lcd.display('would you like atutorial?')
utime.sleep_ms(2500)
lcd.clearLCD()
lcd.display('Right button yesLeft button no')
#button check loop for tutorial
while True:
    checkbuttonstates() 
    
    if debounce(button1) and buttonState1 == 0 and prev_buttonState1 == 1:
        lcd.clearLCD()
        break
    
    if debounce(button4) and buttonState4 == 0 and prev_buttonState4 == 1:
        tutorial()
        lcd.clearLCD()
        break
    prev_buttonState = buttonState1
    prev_buttonState4 = buttonState4
#call game loop
game()