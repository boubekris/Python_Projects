import pygame
from  pygame import mixer
from random_word import RandomWords

r = RandomWords()

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
word = ''
life = 4
found_letter =  ''
clicked = False
found = 0
Pos = {}
foundLetterList = ""

def get_letter(pos):
        x = pos[0]
        y = pos[1]
        for key in Pos :
            if Pos[key][0]-20 <= x <= Pos[key][0]+20 and Pos[key][1]-20 <= y <= Pos[key][1]+20 :
                return key
        return -1


def restartClicked(pos,restartWidth,restartHeight):
    x = pos[0]
    y = pos[1]
    if x in range(400, restartWidth+400) and y in range(500, restartHeight+500):
        return True
    return False

# Get Random word
def selectWord():
    return r.get_random_word().upper()


# Draw The Alphabet
def drawAlphabet():
    
    X=20
    Y=400
    Pos={}
    
    for i in alphabet:
        pygame.draw.circle(screen, (0,0, 255),(X+10,Y+16),20,2)
        Pos[i]=(X+10,Y+16)
        sc = font.render(i, True, (0, 0, 0))
        sc_center = sc.get_rect(center=(X+10, Y+16))
        screen.blit(sc, sc_center)
        X += 60
        if X > 750:
            X = 20
            Y += 60
    return Pos

def restartGame(pos):
    global Pos, word, life, found_letter, clicked, found, foundLetterList
    pygame.draw.rect(screen,(12,12,12),pygame.Rect(400,500,restartWidth,restartHeight),0)
    screen.blit(restart, (400, 500))
    #If Restart clicked
    if restartClicked(pos, restartWidth, restartHeight):
        foundLetterList = ""
        screen.fill((255, 255, 255))
        Pos = drawAlphabet()
        word = selectWord()
        life = 4
        found_letter =  ''
        clicked = False
        found = 0


if __name__ == "__main__":
    # init the game
    pygame.init()

    # create window
    screen = pygame.display.set_mode((800, 600))

    # logo & title
    pygame.display.set_caption("Hangman")
    
    font = pygame.font.Font("freesansbold.ttf", 32)
    running = True
    screen.fill((255, 255, 255))

    restart = font.render('restart' , True , (255,0,0))    
    restartWidth = restart.get_rect().width
    restartHeight = restart.get_rect().height
    
    Pos = drawAlphabet()
    word = selectWord()

    while running:
        
        screen.blit(font.render("You have "+str(life)+" lives", True, (0, 0, 0)), (0,0))
        
        # Draw the gallows
        # Image from vecteezy
        gallows = pygame.image.load("gallows-vector.jpg")
        gallows = pygame.transform.scale(gallows, (300,350))
        screen.blit(gallows, (-30, 30))
        
        '''
        For imporvement we could use a loop with range of lives lost to draw each step
        '''
        person = pygame.image.load("Charactor2-3_generated.jpg")
        person = pygame.transform.scale(person, (650,450))
        if life < 4 :
            # Draw Head
            screen.blit(person, (180, 130),(390,20,60,100))
            if life < 3:
                # Draw Body
                screen.blit(person, (175, 190),(40,120,60,60))
                if life < 2:
                    # Draw Arms
                    screen.blit(person, (135, 190),(0,120,130,135))
                    pygame.draw.rect(screen,(255,255,255),pygame.Rect(180,260,52,90),0)
                    if life < 1:
                        # Draw Legs
                        screen.blit(person, (135, 190),(0,120,130,200))

        l = 30
        w = 15
        xx = 0

        # Show Letters after loss or win
        for i in range(len(word)):
            if life <= 0 or found == len(word):
                screen.blit(font.render("" + str(word[i]), True, (0, 0, 0)), (300+xx, 140))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(300+xx, 180, l,w), 0)
            xx += 50

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONUP:
                # Erase prviously selected letter
                if not clicked:
                    clicked = True
                else:
                    pygame.draw.circle(screen, (255,255,255), (400,300), 40, 0)

                pos = pygame.mouse.get_pos()
                letter = get_letter(pos)
                
                if letter != -1 and letter not in foundLetterList:
                    found_letter = letter
                    foundLetterList += found_letter
                    
                    x,y=Pos[found_letter]
                    # Hide guessed letter
                    pygame.draw.circle(screen, (255, 255, 255), (x,y), 20, 0)
                    
                    # sub life if guessed letter not in word
                    if found_letter not in word :
                        life -=1
                        pygame.draw.rect(screen,(255,255,255),pygame.Rect(0,0,190,32),0)
                    # Show guessed letters
                    else :
                        indexes = [index for index, element in enumerate(word) if element == found_letter]
                        for ii in indexes :
                            found += 1
                            xy = ii*50
                            screen.blit(font.render("" + str(found_letter), True, (0, 0, 0)), (300 + xy, 140))
                # Show found letter above alphabet as the currently guesses one
                if found_letter != '':
                    screen.blit(font.render("" + str(found_letter), True, (0, 0, 0)), (400, 300))            
                
                #Game over
                if life <= 0 :
                    life = 0
                    pygame.draw.rect(screen,(255,255,255),pygame.Rect(0,0,800,600),0)
                    screen.blit(font.render("GAME OVER", True, (0, 0, 0)), (400, 300))

                #win Game
                elif found == len(word):
                    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, 800, 600), 0)
                    screen.blit(font.render("CONGRATULATIONS!!!!!", True, (0, 0, 0)), (350, 300))
                
                #Draw Restart if won or lost
                if life <=0 or found == len(word):
                    restartGame(pos)

        pygame.display.update()
