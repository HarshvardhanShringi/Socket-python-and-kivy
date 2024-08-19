import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import time
import subprocess
import os
import tkinter
import pyautogui


class SocketServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Socket Server")

        # Set up the GUI elements
        self.log_text = scrolledtext.ScrolledText(root, state='disabled', width=50, height=20)
        self.log_text.pack(padx=10, pady=10)

        self.status_label = tk.Label(root, text="Server status: Not running")
        self.status_label.pack(padx=10, pady=5)

        self.start_button = tk.Button(root, text="Start Server", command=self.start_server)
        self.start_button.pack(padx=10, pady=5)

        self.stop_button = tk.Button(root, text="Stop Server", command=self.stop_server, state='disabled')
        self.stop_button.pack(padx=10, pady=5)

        self.server_thread = None
        self.server_running = False
        self.server_socket = None
        self.conn = None
        self.addr = None

    def log_message(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.config(state='disabled')
        self.log_text.yview(tk.END)

    def start_server(self):
        if not self.server_running:
            self.server_running = True
            self.server_thread = threading.Thread(target=self.run_server)
            self.server_thread.start()
            self.status_label.config(text="Server status: Running")
            self.start_button.config(state='disabled')
            self.stop_button.config(state='normal')

    def stop_server(self):
        self.server_running = False
        if self.server_socket:
            self.server_socket.close()
        if self.conn:
            self.conn.close()
        self.status_label.config(text="Server status: Not running")
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')

    def run_server(self):
        host = ""  # Update with the server's IP address
        port = 
        self.server_socket = socket.socket()
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        self.log_message(f"Server listening on {host}:{port}")

        while self.server_running:
            try:
                self.conn, self.addr = self.server_socket.accept()
                self.log_message(f"Connection from: {self.addr}")

                while self.server_running:
                    data = self.conn.recv(1024).decode()
                    if not data:
                        break


                    if data.lower().startswith("open "):
                        app_name = data[5:].strip().lower()
                        if app_name == "chrome":
                            os.startfile("C://ProgramData//Microsoft//Windows//Start Menu//Programs//Google Chrome.lnk")  # Modify as needed for your system
                        elif app_name == "word":
                            os.startfile("C://ProgramData//Microsoft//Windows//Start Menu//Programs//Word.lnk")  # Modify as needed for your system
                        elif app_name == "powerpoint":
                            os.startfile("C://ProgramData//Microsoft//Windows//Start Menu//Programs//PowerPoint.lnk")  # Modify as needed for your system
                        elif app_name == "excel":
                            os.startfile("C://ProgramData//Microsoft//Windows//Start Menu//Programs//Excel.lnk")
                        else:
                            self.log_message(f"Unknown application: {app_name}")

                    elif data.lower().startswith("take "):
                        task_name = data.split(':')[1]
                        if task_name=="screenshot":
                            pyautogui.screenshot(r"C:\Users\DELL\Pictures\Screenshots")


                    elif data.lower().startswith("play "):

                        song_name = data.split(':')[1]
                        music_dir = 'D:\\1. Main\\songs\\new songs'
                        full_path = music_dir + "\\" + song_name + ".mp4"
                        full_path = full_path.replace("\\", "\\\\")

                        try:
                            os.startfile(full_path)
                            self.log_message(f"Playing song {song_name}")

                        except:
                            self.log_message(f"Song not found: {song_name}")

                    self.log_message(f"Received from client: {data}")
                    response = "done"
                    time.sleep(2)  # Simulate some processing delay
                    self.conn.send(response.encode())
            except Exception as e:
                self.log_message(f"Error: {e}")

        if self.conn:
            self.conn.close()


def main():
    root = tk.Tk()
    app = SocketServerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
