import socket

# define game value variables
p1y = 0
p2y = 0
ballx = 500
bally = 300
ballvelx = 1
ballvely = 1

# define server post defualts
normalpost = "HTTP/1.0 200 OK\n\n"

# Define socket host and port
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

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
                    + str(ballvelx)
                    + " "
                    + str(ballvely)
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
                    + str(ballvelx)
                    + " "
                    + str(ballvely)
                )
        elif filename == "/ballpost":
            print("RECIEVED:", filename)
            tballx = headers[7].split()[1]
            tbally = headers[8].split()[1]
            tballvelx = headers[9].split()[1]
            tballvely = headers[10].split()[1]
            if not tballx == ballx:
                ballx = tballx
            if not tbally == bally:
                bally = tbally
            if not tballvelx == ballvelx:
                ballvelx = tballvelx
            if not tballvely == ballvely:
                ballvely = tballvely

            print("ballx", ballx)
            print("bally", bally)
            print("ballvelx", ballvelx)
            print("ballvely", ballvely)

        else:
            response = "HTTP/1.0 400 NOT FOUND\n\nInvalid Page Request"
    except:
        response = "HTTP/1.0 403 NOT FOUND\n\nServer Error :("

    print("RESPONDED:", response)

    # Send HTTP response
    client_connection.sendall(response.encode())
    client_connection.close()

# Close socket
server_socket.close()
