from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Ellipse
import socket
import time
import threading


class MousePointer(Widget):
    def _init_(self, server_conn, **kwargs):
        super(MousePointer, self)._init_(**kwargs)
        self.server_conn = server_conn
        with self.canvas:
            Color(0, 0, 1, 1)  # Blue color for the pointer
            self.pointer = Ellipse(pos=self.center, size=(50, 50))
        self.bind(pos=self.update_pointer)
        self.last_pos = self.center  # Track the last position for smooth movement
        self.movement_lock = threading.Lock()

    def on_touch_move(self, touch):
        # Update the position of the pointer
        self.pos = (touch.x - self.width / 2, touch.y - self.height / 2)

        # Calculate the movement delta for more stable control
        dx = int(touch.dx)
        dy = int(-touch.dy)  # Negative y for correct direction

        # Send the movement command to the server if there is a significant movement
        if abs(dx) > 1 or abs(dy) > 1:
            command = f"MOVE {dx} {dy}"
            threading.Thread(target=self.send_command, args=(command,)).start()

    def send_command(self, command):
        with self.movement_lock:
            try:
                self.server_conn.send(command.encode())
                time.sleep(0.01)  # Slight delay to avoid flooding the server
            except BrokenPipeError:
                print("Connection to server was lost.")
                self.parent.handle_disconnect()

    def update_pointer(self, *args):
        # Update the position of the ellipse when the widget moves
        self.pointer.pos = self.pos


class RemoteMouseApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # TextInput fields for IP address and port number
        self.ip_input = TextInput(hint_text='Enter IP Address', multiline=False, size_hint_y=None, height=50)
        self.port_input = TextInput(hint_text='Enter Port Number', multiline=False, size_hint_y=None, height=50)

        # Connect button
        connect_button = Button(text='Connect', size_hint_y=None, height=50)
        connect_button.bind(on_release=self.connect_to_server)

        # Add the inputs and connect button to the layout
        layout.add_widget(self.ip_input)
        layout.add_widget(self.port_input)
        layout.add_widget(connect_button)

        # Placeholder layout to be replaced with mouse control layout after connection
        self.control_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        layout.add_widget(self.control_layout)

        return layout

    def connect_to_server(self, instance):
        ip_address = self.ip_input.text
        port = int(self.port_input.text)

        # Connect to the server
        self.server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server_conn.connect((ip_address, port))
            print(f"Connected to {ip_address}:{port}")

            # Update the UI with the mouse control layout
            self.control_layout.clear_widgets()

            # Create the mouse pointer widget
            self.pointer = MousePointer(self.server_conn, size=(50, 50))

            # Buttons for mouse clicks
            left_click_button = Button(text='Left Click', size_hint_y=None, height=50)
            left_click_button.bind(on_release=self.on_left_click)

            right_click_button = Button(text='Right Click', size_hint_y=None, height=50)
            right_click_button.bind(on_release=self.on_right_click)

            # Buttons for scrolling
            scroll_up_button = Button(text='Scroll Up', size_hint_y=None, height=50)
            scroll_up_button.bind(on_release=self.on_scroll_up)

            scroll_down_button = Button(text='Scroll Down', size_hint_y=None, height=50)
            scroll_down_button.bind(on_release=self.on_scroll_down)

            # Add the pointer and buttons to the control layout
            self.control_layout.add_widget(self.pointer)
            self.control_layout.add_widget(left_click_button)
            self.control_layout.add_widget(right_click_button)
            self.control_layout.add_widget(scroll_up_button)
            self.control_layout.add_widget(scroll_down_button)
        except Exception as e:
            print(f"Failed to connect: {e}")

    def on_left_click(self, instance):
        # Send the left click command to the server
        command = "CLICK left"
        self.server_conn.send(command.encode())

    def on_right_click(self, instance):
        # Send the right click command to the server
        command = "CLICK right"
        self.server_conn.send(command.encode())

    def on_scroll_up(self, instance):
        # Send the scroll up command to the server
        command = "SCROLL 20"  # Positive value for scrolling up
        self.server_conn.send(command.encode())

    def on_scroll_down(self, instance):
        # Send the scroll down command to the server
        command = "SCROLL -20"  # Negative value for scrolling down
        self.server_conn.send(command.encode())

    def handle_disconnect(self):
        # Handle disconnection gracefully, notify the user or attempt to reconnect
        print("Handling disconnection...")

    def on_stop(self):
        # Close the connection when the app stops
        if hasattr(self, 'server_conn'):
            self.server_conn.close()


if _name_ == '_main_':
    RemoteMouseApp().run()
