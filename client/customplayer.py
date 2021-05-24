from clientnetworking import clientRequest
import pygame
import time
import random

# username = input("Please type a username: ")
pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("HTTPONG")
font = pygame.font.Font("freesansbold.ttf", 32)
clock = pygame.time.Clock()
playerID = input("which player are you? 1 or 2: ")
# playerID = "1"
posY = 300
color = (255, 255, 255)
paddleWidth = 5
paddleHeight = 5
otherPlayerY = 300
networkingInterface = clientRequest("http://192.168.86.55:7676/", playerID, str(posY))


def game_loop():
    posY = 300
    pressed_up = False
    pressed_down = False
    while True:
        try:
            for event in pygame.event.get():
                # Add some extra ways to exit the game.
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                elif event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:  # check for key presses
                    if event.key == pygame.K_UP:  # up arrow goes up
                        pressed_up = True
                    elif event.key == pygame.K_DOWN:  # down arrow goes down
                        pressed_down = True
                elif event.type == pygame.KEYUP:  # check for key releases
                    if event.key == pygame.K_UP:  # up arrow goes up
                        pressed_up = False
                    elif event.key == pygame.K_DOWN:  # down arrow goes down
                        pressed_down = False

            if pressed_up:
                posY -= 10
            if pressed_down:
                posY += 10

            # Redraw the screen.
            screen.fill((0, 0, 0))

            # ==============================================================================

            # post request our position and get the game data from the server
            requestData = networkingInterface.postValues(posY).split()
            otherPlayerY = requestData[0].strip("b'")
            ballX = int(requestData[1])
            ballY = int(requestData[2])
            p1score = requestData[3]
            p2score = requestData[4].strip("'")

            # ==============================================================================
            # posY = random.randint(0, 600)
            # draw our player on the screen
            if playerID == "1":  # if player 1
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(
                        0,
                        int(posY) - 50,
                        paddleWidth,
                        100,
                    ),
                )
            else:
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(
                        995,
                        int(posY) - 50,
                        paddleWidth,
                        100,
                    ),
                )

            # draw our enemy on the screen
            if playerID == "1":
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(
                        995,
                        int(otherPlayerY) - 50,
                        paddleWidth,
                        100,
                    ),
                )
            else:
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(
                        0,
                        int(otherPlayerY) - 50,
                        paddleWidth,
                        100,
                    ),
                )
            pygame.draw.circle(screen, color, (int(ballX), int(ballY)), 5)
            # ==============================================================================

            # render our current score to the screen
            text = font.render(p1score + " to " + p2score, True, color)
            textRect = text.get_rect()
            textRect.center = (500, 300)
            screen.blit(text, textRect)

            # ==============================================================================

            pygame.display.flip()
            clock.tick(30)
            time.sleep(0.1)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    # networkingInterface.connect(username) TODO
    game_loop()
