from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import socket
import ipaddress
from kivy.core.window import Window



Window.size = (350, 600)

Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        Button:
            text: 'Connect'
            on_press: root.pressed(self)
            size: 95, 50
            size_hint: None, None
            pos:60,100
        
<SettingsScreen>:
    BoxLayout:
        
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
            size: 95, 50
            size_hint: None, None
        Button:
            text: 'Send'
            on_press: root.sending(self)
            size: 95, 50
            size_hint: None, None
            pos_hint_x: None
            pos:100,200
            
""")

# Declare both screens
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.cols = 1

        self.inside = GridLayout()
        self.inside.cols = 2

        self.inside.add_widget(Label(text="IP Address: ",size_hint_y=None,height=50))
        self.ipaddress = TextInput(multiline=False,font_size=20,background_color='#FFFFE4E1',size_hint_y=None,height=50)
        self.inside.add_widget(self.ipaddress)

        self.inside.add_widget(Label(text="Port no: ",size_hint_y=None,height=50))
        self.portno = TextInput(multiline=False,font_size=20,background_color='#FFFFE4E1',size_hint_y=None,height=50)
        self.inside.add_widget(self.portno)


        self.inside.add_widget(Label(text="Name Pass: ",size_hint_y=None,height=50))
        self.passs = TextInput(multiline=False,password_mask="*",password=True,font_size=20,background_color='#FFFFE4E1',size_hint_y=None,height=50)
        self.inside.add_widget(self.passs)

        self.add_widget(self.inside)

        self.submit = Button(text="Connect", font_size=10,pos_hint= {'center_x':1, 'center_y':2},size_hint=(0.1,0.1),height=50)
        self.submit.bind(on_press=self.pressed)
        self.add_widget(self.submit)

    def chatting(self, **kwargs):
        print('connecting to server..')
        sm.current='settings'

    def scket(self):
        global c
        c = socket.socket()
        c.connect((ip, 56668))
        #print(c.recv(1024).decode())
        c.sendto(bytes(name_, 'utf-8'),(ip,int(prt)))

        #c.send(bytes(prt, 'utf-8'))
        #print(c.recv(1024).decode())
        if pas=="Hukam":
            self.inside.add_widget(Label(text=c.recv(1024).decode(), size_hint_y=None, font_size=10,
                                         pos_hint={'center_x': 0.6, 'center_y': 2}, size_hint=(0.1, 0.1), height=50))
            self.chatting()

    def pressed(self, instance):
        global ip,prt,passs1,name_,pas
        ip = self.ipaddress.text
        prt = self.portno.text
        #name_ = self.name.text
        passs1 = self.passs.text

        name_,pas=passs1.split()

        #print("IP Address:", ip, "Port no:", prt, "Name:", name_,"Password",passs1)
        self.scket()

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen,self).__init__(**kwargs)
        self.cols = 1
        self.rows=2
        self.inside = GridLayout()
        self.inside.cols = 2
        self.inside.add_widget(Label(text="Dell ^_^ ", size_hint_y=None, height=40))
        self.messag = TextInput(multiline=False, font_size=20,size_hint_y=None, background_color='#FFFFE4E1')
        self.inside.add_widget(self.messag)
        self.add_widget(self.inside)

    def sending(self,instance):
        global msg
        msg=self.messag.text
        c.sendto(bytes(msg, 'utf-8'), (ip, int(prt)))

class TestApp(App):

    def build(self):
        # Create the screen manager
        global sm
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))

        return sm

if __name__ == '__main__':
    TestApp().run()
