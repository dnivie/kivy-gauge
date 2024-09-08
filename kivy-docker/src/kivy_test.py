import time
import kivy
kivy.require('2.3.0') # replace with your current kivy version !


from kivy.app import App
from kivy.uix.label import Label
file_path = "/tmp/testfile"

class MyApp(App):

    def build(self):
        return Label(text='Hello world')

    def read(self):
        with open(file_path, 'r') as file:
            data = file.read()
        print(data)
        time.sleep(0.5)


if __name__ == '__main__':
    MyApp().run()
