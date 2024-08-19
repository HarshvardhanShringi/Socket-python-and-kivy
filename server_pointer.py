import socket
import threading
import pyautogui
import tkinter as tk

class RemoteMouseServer:
    def __init__(self, master):
        self.master = master
        self.master.title("Remote Mouse Server")

        # Fixed IP and Port
        self.ip_address = "192.168.115.148"
        self.port = 57320

        # Initialize server variables
        self.server = None
        self.conn = None
        self.addr = None
        self.running = False

        # Status Message Label
        self.status_label = tk.Label(master, text="Server not started", fg="red")
        self.status_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Start Server Button
        self.start_button = tk.Button(master, text="Start Server", command=self.start_server)
        self.start_button.grid(row=1, column=0, padx=10, pady=10)

        # Stop Server Button
        self.stop_button = tk.Button(master, text="Stop Server", command=self.stop_server, state=tk.DISABLED)
        self.stop_button.grid(row=1, column=1, padx=10, pady=10)

    def update_status(self, message, color):
        self.status_label.config(text=message, fg=color)

    def start_server(self):
        # Start the server in a new thread
        if not self.running:
            self.server_thread = threading.Thread(target=self.run_server)
            self.server_thread.start()
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.update_status("Server starting...", "orange")
        else:
            self.update_status("Server is already running.", "red")

    def stop_server(self):
        if self.running:
            self.running = False
            if self.conn:
                self.conn.close()
            if self.server:
                self.server.close()
            self.server_thread.join()
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.update_status("Server stopped.", "red")

    def run_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip_address, self.port))
        self.server.listen(1)
        print(f"Server listening on {self.ip_address}:{self.port}")

        try:
            self.conn, self.addr = self.server.accept()
            print("Connected to client")
            self.update_status("Connected to client", "green")

            while self.running:
                try:
                    data = self.conn.recv(1024).decode()
                    if not data:
                        break

                    command = data.split()

                    if command[0] == "MOVE" and len(command) == 3:
                        # MOVE x y
                        try:
                            x, y = int(command[1]) * 2, int(command[2]) * 2  # Increase movement speed
                            pyautogui.moveRel(x, y)
                        except ValueError:
                            print(f"Invalid MOVE command: {data}")
                    elif command[0] == "CLICK" and len(command) == 2:
                        # CLICK left/right
                        button = command[1]
                        pyautogui.click(button=button)
                    elif command[0] == "SCROLL" and len(command) == 2:
                        # SCROLL up/down amount
                        try:
                            amount = int(command[1])
                            pyautogui.scroll(amount)
                        except :
                            pass
                    else:
                        pass

                except Exception as e:
                    print(f"Error: {e}")
                    break
        finally:
            if self.conn:
                self.conn.close()
            if self.server:
                self.server.close()
            self.update_status("Disconnected.", "red")

if __name__ == "__main__":
    root = tk.Tk()
    app = RemoteMouseServer(root)
    root.mainloop()
