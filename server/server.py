import socket

# define game value variables
p1y = 0
p2y = 0
ballx = 500
bally = 300
ballvelx = 10
ballvely = 10
p1points = 0
p2points = 0
# define server post defualts
normalpost = "HTTP/1.0 200 OK\n\n"

# Define socket host and port
SERVER_HOST = "192.168.86.55"
SERVER_PORT = 7676

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print("Listening on port %s ..." % SERVER_PORT)

while True:
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    request = client_connection.recv(1024).decode()

    # Parse HTTP headers
    headers = request.split("\n")
    # print("HEADERS:", headers)

    filename = headers[0].split()[1]

    try:
        if filename == "/clientupdate":
            # read headers to determine our current player and their values
            currentPlayer = headers[6].split()[1]
            currentPlayerY = headers[7].split()[1]

            # update ball position this frame
            ballx += ballvelx
            bally += ballvely

            # fix shit TODO fix this lol
            p1y = int(p1y)
            p2y = int(p2y)

            # preform checks on ball
            if bally >= 600:  # if ball under screen
                ballvely = -ballvely
            elif bally <= 0:
                ballvely = -ballvely

            if ballx >= 1000:
                if bally >= p2y - 50 and bally <= p2y + 50:
                    ballvelx = -ballvelx
                else:
                    p1points += 1
                    ballx = 500
                    bally = 300

            elif ballx <= 0:
                if bally >= p1y - 50 and bally <= p1y + 50:
                    ballvelx = -ballvelx
                else:
                    p2points += 1
                    ballx = 500
                    bally = 300

            # update our game values from our post requests
            # if the request comes from p1 send p2s data and the ball data
            if currentPlayer == "1":
                p1y = currentPlayerY
                response = (
                    normalpost
                    + str(p2y)
                    + " "
                    + str(ballx)
                    + " "
                    + str(bally)
                    + " "
                    + str(p1points)
                    + " "
                    + str(p2points)
                )
            # if the request comes from p2 send p1s data and the ball data
            elif currentPlayer == "2":
                p2y = currentPlayerY
                response = (
                    normalpost
                    + str(p1y)
                    + " "
                    + str(ballx)
                    + " "
                    + str(bally)
                    + " "
                    + str(p1points)
                    + " "
                    + str(p2points)
                )
        ##elif filename == "/clientconnect": TODO matchmaking system

        else:
            response = "HTTP/1.0 400 NOT FOUND\n\nInvalid Page Request"
    except Exception as e:
        response = "HTTP/1.0 403 NOT FOUND\n\nServer Error :("
        print(e)

    print("RESPONDED:", response)

    # Send HTTP response
    client_connection.sendall(response.encode())
    client_connection.close()

# Close socket
server_socket.close()
