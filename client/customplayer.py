from clientnetworking import clientRequest
import pygame
import time
import random

pygame.init()
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()
# playerID = input("which player are you? 1 or 2: ")
playerID = "1"
posY = 300
color = (255, 255, 255)
paddleWidth = 5
paddleHeight = 5
otherPlayerY = 300
networkingInterface = clientRequest("http://127.0.0.1:8000/", playerID, str(posY))


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
            ballVelX = requestData[3]
            ballVelY = requestData[4].strip("'")

            # ==============================================================================
            # posY = random.randint(0, 600)
            # draw our player on the screen
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(
                    0,
                    posY + 50,
                    paddleWidth,
                    100,
                ),
            )
            # draw our enemy on the screen
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(
                    995,
                    int(otherPlayerY) + 50,
                    paddleWidth,
                    100,
                ),
            )
            pygame.draw.circle(screen, color, (ballX, ballY), 5)
            # ==============================================================================
            if playerID == "1":
                ballX += int(ballVelX)
                ballY += int(ballVelY)
            else:
                ballX += ballVelX
                ballY += ballVelY

            networkingInterface.postBall(ballX, ballY, ballVelX, ballVelY)
            # ==============================================================================

            pygame.display.flip()
            clock.tick(30)
            time.sleep(0.1)
        except:
            print("server probably timed out D:")


if __name__ == "__main__":
    game_loop()
