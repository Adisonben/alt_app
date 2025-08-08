import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window

Builder.load_file('style/helloworld.kv')

class MyGridLayout(Widget):
    def press(self):
        #create var
        name = self.ids.name_input.text
        
        # update label
        self.ids.name_label.text = f'Hello {name}!'

        #clear input box
        self.ids.name_input.text = ''

class HelloWorldApp(App):
    def build(self):
        # Window.clearcolor = (1,1,1,1) #change bg window color
        return MyGridLayout()
    
if __name__ == '__main__':
    HelloWorldApp().run()