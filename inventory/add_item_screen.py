
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex



back_light_grey = (211/255,211/255,211/255, 1)
light_grey = hex("#F3F2ED")
green = hex("#01311F")
yellow = hex("#C6AA58")
red = hex("#FF0000")
dark_red = hex("#7f0000")


class AddItemScreen(Screen):
    def __init__(self, **kwargs):
        super(AddItemScreen, self).__init__(**kwargs)

        self.window_width, self.window_height = Window.size
        Window.bind(on_resize=self.update_window_size)

        self.layout = FloatLayout()


        # Create Top Banner
        self.layout.top_label = Button(
            text="Add Item", 
            color=(1,1,1,1), 
            size_hint=(1, 0.15), 
            pos_hint={"x": 0, "y": 0.85},
            disabled=True,
            disabled_color=(1,1,1,1),
            background_color=green,
            background_normal = ""
        )
        self.layout.top_label.background_disabled_normal = self.layout.top_label.background_normal
        self.layout.add_widget(self.layout.top_label)



        # Create Labels

        self.layout.name_label = Button(
            text = "Name",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            background_color = yellow,
            size_hint = (0.4, 0.15),
            pos_hint = {"x": 0.1, "y": 0.625},
            background_normal = ""
        )
        self.layout.name_label.background_disabled_normal = self.layout.name_label.background_normal
        self.layout.add_widget(self.layout.name_label)


        self.layout.hourly_rate_label = Button(
            text = "Hourly Rate(s)",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            background_color = yellow,
            size_hint = (0.4, 0.15),
            pos_hint = {"x": 0.1, "y": 0.425},
            background_normal = ""
        )
        self.layout.hourly_rate_label.background_disabled_normal = self.layout.hourly_rate_label.background_normal
        self.layout.add_widget(self.layout.hourly_rate_label)


        self.layout.stock_label = Button(
            text = "Stock",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            background_color = yellow,
            size_hint = (0.4, 0.15),
            pos_hint = {"x": 0.1, "y": 0.225},
            background_normal = ""
        )
        self.layout.stock_label.background_disabled_normal = self.layout.stock_label.background_normal
        self.layout.add_widget(self.layout.stock_label)





        # Create Text Inputs

        self.layout.box_for_name_text = GridLayout(
            rows = 1,
            cols = 1,
            pos_hint = {"x": 0.5, "y": 0.625},
            size_hint = (0.4, 0.15)
        )
        self.layout.name_text_input = TextInput(
            multiline = False,
            halign = "center",
            padding_y = self.window_height * 0.15 * 0.4
        )
        self.layout.box_for_name_text.add_widget(self.layout.name_text_input)
        self.layout.add_widget(self.layout.box_for_name_text)


        self.layout.box_for_rate_text = GridLayout(
            rows = 1,
            cols = 1,
            pos_hint = {"x": 0.5, "y": 0.425},
            size_hint = (0.4, 0.15)
        )
        self.layout.rate_text_input = TextInput(
            multiline = False,
            halign = "center",
            padding_y = self.window_height * 0.15 * 0.4
        )
        self.layout.box_for_rate_text.add_widget(self.layout.rate_text_input)
        
        self.layout.add_widget(self.layout.box_for_rate_text)
        

        self.layout.box_for_stock_text = GridLayout(
            rows = 1,
            cols = 1,
            pos_hint = {"x": 0.5, "y": 0.225},
            size_hint = (0.4, 0.15)
        )
        self.layout.stock_text_input = TextInput(
            multiline = False,
            halign = "center",
            padding_y = self.window_height * 0.15 * 0.4
        )
        self.layout.box_for_stock_text.add_widget(self.layout.stock_text_input)
        
        self.layout.add_widget(self.layout.box_for_stock_text)



        # Error Messages
        
        self.layout.error_rate_label = Button(
            text="Invalid Prices List.", 
            disabled = True,
            disabled_color = red,
            background_color=back_light_grey, 
            size_hint=(0.4, 0.05), 
            pos_hint={"x": 0.5, "y": 0.575},
            background_normal = "",
        )
        self.layout.error_rate_label.background_disabled_normal = self.layout.error_rate_label.background_normal


        self.layout.error_stock_label = Button(
            text="Invalid Stock Number.", 
            disabled = True,
            disabled_color = red,
            background_color=back_light_grey, 
            size_hint=(0.4, 0.05), 
            pos_hint={"x": 0.5, "y": 0.375},
            background_normal = "",
        )
        self.layout.error_stock_label.background_disabled_normal = self.layout.error_stock_label.background_normal


        self.layout.error_add_label = Button(
            text="Item Already Exists.", 
            disabled = True,
            disabled_color = red,
            background_color=back_light_grey, 
            size_hint=(0.4, 0.075), 
            pos_hint={"x": 0.3, "y": 0.15},
            background_normal = "",
        )
        self.layout.error_add_label.background_disabled_normal = self.layout.error_add_label.background_normal




        #Create Buttons
        self.layout.cancel_btn = Button(
            text="Cancel", 
            background_color=green, 
            size_hint=(0.5, 0.15), 
            pos_hint={"x": 0, "y": 0},
            background_normal = ""
        )
        self.layout.add_widget(self.layout.cancel_btn)


        self.layout.add_item_btn = Button(
            text="Add", 
            background_color=green, 
            size_hint=(0.5, 0.15),
            pos_hint={"x": 0.5, "y": 0},
            background_normal = ""
        )
        self.layout.add_widget(self.layout.add_item_btn)



        # Add layout to Inventory Screen
        self.add_widget(self.layout)



    def update_window_size(self, instance, width, height):
        self.window_width = width 
        self.window_height = height



    def get_item_values(self):

        name = str(self.layout.name_text_input.text)
        rate = str(self.layout.rate_text_input.text)
        stock = str(self.layout.stock_text_input.text)

        return {"item_name": name, "hourly_rate": rate, "stock": stock}
    

    @staticmethod
    def verify_rate_entry(hourly_rate):
        # valid entries look like "1, 2, 3 - 4" or "1, 2"
        
        input = hourly_rate
        if input == "":
            return False

        input_no_spaces = ""
        for char in input:
            if char != " ":
                input_no_spaces += char 


        if "-" in input_no_spaces:
            if input_no_spaces.count("-") > 1:
                return False

            daily_rate = input_no_spaces.split("-")[1]

            try:
                daily_rate = float(daily_rate)
                if daily_rate < 0:
                    return False
            except:
                return False 
            
            input_no_spaces = input_no_spaces.split("-")[0]

        nums = input_no_spaces.split(",")
        try:
            for num in nums:
                num = float(num)
                if num < 0:
                    return False
        except:
            return False
        
        return True


    
    def parse_rate_entry(self, hourly_rate):
        # if the rate looks like "1, 2, 3" returns [["1", "2", "3"], ""]
        # if the rate looks like "1, 2 - 3" returns [["1", "2"], "3"]
        if not self.verify_rate_entry(hourly_rate):
            raise ValueError("Invalid rate entry.")
        
        return_list = []
        hourly_rates_list = []
        
        input = hourly_rate

        input_no_spaces = ""
        for char in input:
            if char != " ":
                input_no_spaces += char 

        if "-" in input_no_spaces:
            daily_rate = input_no_spaces.split("-")[1]
            hourly_rates_list = input_no_spaces.split("-")[0].split(",")
            
            return_list = [hourly_rates_list, daily_rate]

        else:
            hourly_rates_list = input_no_spaces.split(",")
            return_list = [hourly_rates_list, ""]       

        return return_list
    

    @staticmethod
    def verify_stock_entry(stock):
        try:
            stock = int(stock)
            if stock < 0:
                return False
        except:
            return False 
        
        return True

        

