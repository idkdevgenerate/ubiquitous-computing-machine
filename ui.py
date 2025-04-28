import tkinter as tk
from tkinter import ttk
import socket

def encrypt_data(data):
    # Placeholder for encryption logic
    return data

def decrypt_data(data):
    # Placeholder for decryption logic
    return data

def send_request_to_proxy(request):
    try:
        # Connect to the proxy server
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.connect(("127.0.0.1", 8888))

        # Encrypt and send the request
        encrypted_request = encrypt_data(request.encode())
        proxy_socket.send(encrypted_request)

        # Receive and decrypt the response
        encrypted_response = proxy_socket.recv(4096)
        response = decrypt_data(encrypted_response).decode()
        proxy_socket.close()
        return response
    except Exception as e:
        return f"Error: {e}"

def create_ui():
    root = tk.Tk()
    root.title("Smooth UI")
    root.geometry("800x600")

    # Create a search bar at the top
    search_frame = tk.Frame(root, bg="lightgray", height=50)
    search_frame.pack(side=tk.TOP, fill=tk.X)

    search_label = tk.Label(search_frame, text="Search:", bg="lightgray")
    search_label.pack(side=tk.LEFT, padx=10, pady=10)

    search_entry = tk.Entry(search_frame, width=50)
    search_entry.pack(side=tk.LEFT, padx=10, pady=10)

    def on_search():
        query = search_entry.get()
        if query:
            response = send_request_to_proxy(query)
            content_label.config(text=response)

    def on_search_people():
        query = search_entry.get()
        if query:
            # Example request format for searching people
            request = f"GET /search_people?query={query} HTTP/1.1\r\nHost: crazygames.com\r\n\r\n"
            response = send_request_to_proxy(request)
            content_label.config(text=response)

    search_button = tk.Button(search_frame, text="Go", command=on_search)
    search_button.pack(side=tk.LEFT, padx=10, pady=10)

    # Add a new button for searching people
    people_search_button = tk.Button(search_frame, text="Search People", command=on_search_people)
    people_search_button.pack(side=tk.LEFT, padx=10, pady=10)

    # Create tabs on the left
    tabs_frame = tk.Frame(root, bg="lightblue", width=200)
    tabs_frame.pack(side=tk.LEFT, fill=tk.Y)

    tabs = ["Home", "Settings", "About"]
    for tab in tabs:
        tab_button = tk.Button(tabs_frame, text=tab, bg="white", relief=tk.FLAT)
        tab_button.pack(fill=tk.X, padx=5, pady=5)

    # Add a game selection interface
    game_frame = tk.Frame(root, bg="white")
    game_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    game_label = tk.Label(game_frame, text="Select a Game:", bg="white")
    game_label.pack()

    game_listbox = tk.Listbox(game_frame)
    games = ["Game 1", "Game 2", "Game 3"]
    for game in games:
        game_listbox.insert(tk.END, game)
    game_listbox.pack()

    def on_launch_game():
        selected_game = game_listbox.get(tk.ACTIVE)
        if selected_game:
            response = send_request_to_proxy(f"LAUNCH {selected_game}")
            content_label.config(text=response)

    launch_button = tk.Button(game_frame, text="Launch Game", command=on_launch_game)
    launch_button.pack(pady=10)

    # Main content area
    content_frame = tk.Frame(root, bg="white")
    content_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

    content_label = tk.Label(content_frame, text="Welcome to the Smooth UI!", bg="white", font=("Arial", 16))
    content_label.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_ui()