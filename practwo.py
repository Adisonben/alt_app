from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

#Define our diff screens
class FirstWindow(Screen):
    pass

class SecondWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('style/multiscreen.kv')

# class MyLayout(Widget):
#     #pass
#     checks = []
#     # Checkbox
#     def checkbox_clicked(self, instance, value, content):
#         if value == True:
#             MyLayout.checks.append(content)
#         else:
#             MyLayout.checks.remove(content)
        
#         if len(MyLayout.checks) > 0:
#             tops = ''
#             for x in MyLayout.checks:
#                 tops = f'{tops} {x}'
#             self.ids.output_label.text = f'Selected: {tops}'
#         else:
#             self.ids.output_label.text = 'Please select a checkbox'

#     #slider
#     def slide_it(self, *args):
#         self.slide_text.text = str(int(args[1]))
#         self.slide_text.font_size = str(int(args[1]) * 5)

#     #image viewer & file chooser
#     def selected(self, filename):
#         try:
#             self.ids.my_image.source = filename[0]
#             print("Selected file: ", filename[0])

#         except:
#             pass

class AwesomeApp(App):
    def build(self):
        Window.clearcolor = (0,0,0,1)
        return kv
    
if __name__ == '__main__':
    AwesomeApp().run()