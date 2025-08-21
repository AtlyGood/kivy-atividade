from kivy.app import App
from kivy.uix.label import Label

class HelloWordApp(App):
    def build(self):
        return Label(text="hello word")

if __name__ == "__main__":
    HelloWordApp().run()