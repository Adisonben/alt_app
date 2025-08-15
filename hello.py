import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window

#set app size
Window.size=(500,700)

Builder.load_file('style/helloworld.kv')

class MyGridLayout(Widget):
    def clear(self):
        self.ids.calc_input.text = '0'
        
    def button_press(self, button):
        #create var that contains whatever was in text box already
        prior = self.ids.calc_input.text

        if "error" in prior:
            prior = ''

        # determine if 0 is sitting there
        if prior == "0":
            self.ids.calc_input.text = ''
            self.ids.calc_input.text = f'{button}'
        else:
            self.ids.calc_input.text = f'{prior}{button}'

    # addition function
    def math_sign(self, sign):
        #create var that contains whatever was in text box already
        prior = self.ids.calc_input.text
        #slap a plus sign
        self.ids.calc_input.text = f'{prior}{sign}'

    def remove(self):
        prior = self.ids.calc_input.text
        prior = prior[:-1]
        if prior == "":
            self.ids.calc_input.text = "0"
        else:
            self.ids.calc_input.text = prior

    def pos_neg(self):
        prior = self.ids.calc_input.text
        if "-" in prior:
            self.ids.calc_input.text = f'{prior.replace("-", "")}'
        else:
            self.ids.calc_input.text = f'-{prior}'


    def dot(self):
        prior = self.ids.calc_input.text
        num_list = prior.split("+")
        
        if "+" in prior and "." not in num_list[-1]:
            prior = f'{prior}.'
            self.ids.calc_input.text = prior

        elif "." in prior:
            pass
        else:
            prior = f'{prior}.'
            self.ids.calc_input.text = prior

    # create equls to function
    def equals(self):
        prior = self.ids.calc_input.text

        #error handling
        try:
            answer = eval(prior)
            self.ids.calc_input.text = str(answer)
        except:
            self.ids.calc_input.text = "error"

        """
        #addition
        if "+" in prior:
            num_list = prior.split("+")
            answer = 0.0
            # loop thru our list
            for number in num_list:
                answer = answer + float(number)

            #print answer in text box
            self.ids.calc_input.text = str(answer)
        """

class HelloWorldApp(App):
    def build(self):
        # Window.clearcolor = (1,1,1,1) #change bg window color
        return MyGridLayout()
    
if __name__ == '__main__':
    HelloWorldApp().run()