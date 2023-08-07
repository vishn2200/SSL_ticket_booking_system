import socket
import os
import ssl

cf = os.path.join("certs", "server.crt")
kf = os.path.join("certs", "server.key")

# Server configuration
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile= cf, keyfile= kf)
host = "localhost"
port = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)
# Movie database
movies = {
    "1": {"name": "The Truman Show", "seats": 100, "price": 10},
    "2": {"name": "Avatar", "seats": 50, "price": 8},
    "3": {"name": "Alien", "seats": 200, "price": 12},
}


print("Server is listening on {}:{}".format(host, port))

while True:
    client_socket, addr = server_socket.accept()
    conn = context.wrap_socket(client_socket, server_side=True)

    # Send movie details to client
    movie_data = ""
    for movie_id, movie_info in movies.items():
        movie_data += "{}. {} (Seats: {}, Price: ${})\n".format(
            movie_id, movie_info["name"], movie_info["seats"], movie_info["price"]
        )
    conn.sendall(movie_data.encode())

    # Receive data from client
    data = conn.recv(1024)
    data = data.decode()
    selected_movie_id, num_tickets = data.split("#")

    # Check if selected movie is valid
    if selected_movie_id not in movies.keys():
        response = "Invalid movie selection."
    elif int(num_tickets) > movies[selected_movie_id]["seats"]:
        response = "Not enough seats available."
    else:
        # Update movie details
        movies[selected_movie_id]["seats"] -= int(num_tickets)
        total_price = movies[selected_movie_id]["price"] * int(num_tickets)
        response = "Booking successful! Total Price: ${}".format(total_price)

    # Send response to client
    conn.sendall(response.encode())
