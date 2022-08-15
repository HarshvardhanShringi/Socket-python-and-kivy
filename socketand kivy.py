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


class MyGrid2(GridLayout):
    def __init__(self, **kwargs):
        print('MyGrid2')
        super(MyGrid2, self).__init__(**kwargs)
        self.cols = 1

        self.inside = GridLayout()
        self.inside.cols = 2

        self.inside.add_widget(Label(text="Dell: "))
        self.dell = TextInput(multiline=False)
        self.inside.add_widget(self.dell)


class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 1

        self.inside = GridLayout()
        self.inside.cols = 2

        self.inside.add_widget(Label(text="IP Address: "))
        self.ipaddress = TextInput(multiline=False)
        self.inside.add_widget(self.ipaddress)

        self.inside.add_widget(Label(text="Port no: "))
        self.portno = TextInput(multiline=False)
        self.inside.add_widget(self.portno)

        self.inside.add_widget(Label(text="Name: "))
        self.name = TextInput(multiline=False)
        self.inside.add_widget(self.name)

        self.inside.add_widget(Label(text="Passowrd: "))
        self.passs = TextInput(multiline=False)
        self.inside.add_widget(self.passs)

        self.add_widget(self.inside)

        self.submit = Button(text="Submit", font_size=30)
        self.submit.bind(on_press=self.pressed)
        self.add_widget(self.submit)

    def chatting(self, **kwargs):
        print('Opening chatbox')





    def scket(self):
        c = socket.socket()
        c.connect((ip, 56668))
        #print(c.recv(1024).decode())
        c.sendto(bytes(name_, 'utf-8'),(ip,int(prt)))

        #c.send(bytes(prt, 'utf-8'))
        #print(c.recv(1024).decode())
        if passs1=="Hukam":
            self.chatting()






    def pressed(self, instance):
        global ip,prt,name_,passs1
        ip = self.ipaddress.text
        prt = self.portno.text
        name_ = self.name.text
        passs1 = self.passs.text


        #print("IP Address:", ip, "Port no:", prt, "Name:", name_,"Password",passs1)
        self.scket()


class MyApp(App):
    def build(self):
        return MyGrid()



if __name__ == "__main__":
    MyApp().run()
