import socket
import ssl
import tkinter as tk
from tkinter import messagebox

# Create main window
root = tk.Tk()
root.title("Movie Ticket Booking System")

# Function to handle button click event
def book_ticket():
    # Server configuration
    context = ssl._create_unverified_context()
    host = 'localhost'
    port = 8080

    # Create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn=context.wrap_socket(client_socket,server_hostname=host)
    conn.connect((host, port))
    
    response = conn.recv(1024)
    response = response.decode()
    
    # Show response in a message box
    messagebox.showinfo("Booking Status", response)
    
    # Get user input
    movie_name = movie_name_entry.get()
    num_tickets = num_tickets_entry.get()
    
    # Send data to server
    data = "{}#{}".format(movie_name, num_tickets)
    conn.sendall(data.encode())
    
    # Receive data from server
    response = conn.recv(1024)
    response = response.decode()
    
    # Show response in a message box
    messagebox.showinfo("Booking Status", response)
    
    # Close client socket
    conn.close()
# Create UI components
movie1=tk.Label(root, text="1- The Truman Show")
movie1.pack()
movie2=tk.Label(root, text="2- Avatar")
movie2.pack()
movie3=tk.Label(root, text="3- Alien")
movie3.pack()
movie_name_label = tk.Label(root, text="Movie ID:")
movie_name_label.pack()
movie_name_entry = tk.Entry(root)
movie_name_entry.pack()

num_tickets_label = tk.Label(root, text="Number of Tickets:")
num_tickets_label.pack()
num_tickets_entry = tk.Entry(root)
num_tickets_entry.pack()

book_button = tk.Button(root, text="Book Ticket", command=book_ticket)
book_button.pack()

# Start main event loop
root.mainloop()