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


class EditItemScreen(Screen):
    def __init__(self, associated_item, **kwargs):
        super(EditItemScreen, self).__init__(**kwargs)

        self.associated_item = associated_item

        self.window_width, self.window_height = Window.size
        Window.bind(on_resize=self.update_window_size)

        self.layout = FloatLayout()


        # Create Top Banner
        self.layout.top_label = Button(
            text="Edit Item", 
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

        self.layout.item_no_label = Button(
            text = "New Item Number",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            background_color = yellow,
            size_hint = (0.4, 0.1),
            pos_hint = {"x": 0.1, "y": 0.675},
            background_normal = ""
        )
        self.layout.item_no_label.background_disabled_normal = self.layout.item_no_label.background_normal
        self.layout.add_widget(self.layout.item_no_label)


        self.layout.name_label = Button(
            text = "New Name",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            background_color = yellow,
            size_hint = (0.4, 0.1),
            pos_hint = {"x": 0.1, "y": 0.525},
            background_normal = ""
        )
        self.layout.name_label.background_disabled_normal = self.layout.name_label.background_normal
        self.layout.add_widget(self.layout.name_label)


        self.layout.hourly_rate_label = Button(
            text = "New Hourly Rate(s)",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            background_color = yellow,
            size_hint = (0.4, 0.1),
            pos_hint = {"x": 0.1, "y": 0.375},
            background_normal = ""
        )
        self.layout.hourly_rate_label.background_disabled_normal = self.layout.hourly_rate_label.background_normal
        self.layout.add_widget(self.layout.hourly_rate_label)


        self.layout.stock_label = Button(
            text = "New Stock",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            background_color = yellow,
            size_hint = (0.4, 0.1),
            pos_hint = {"x": 0.1, "y": 0.225},
            background_normal = ""
        )
        self.layout.stock_label.background_disabled_normal = self.layout.stock_label.background_normal
        self.layout.add_widget(self.layout.stock_label)





        # Create Text Inputs

        self.layout.box_for_item_no_text = GridLayout(
            rows = 1,
            cols = 1,
            pos_hint = {"x": 0.5, "y": 0.675},
            size_hint = (0.4, 0.1)
        )
        self.layout.item_no_text_input = TextInput(
            multiline = False,
            halign = "center",
            padding_y = self.window_height * 0.1 * 0.3
        )
        self.layout.box_for_item_no_text.add_widget(self.layout.item_no_text_input)
        self.layout.add_widget(self.layout.box_for_item_no_text)



        self.layout.box_for_name_text = GridLayout(
            rows = 1,
            cols = 1,
            pos_hint = {"x": 0.5, "y": 0.525},
            size_hint = (0.4, 0.1)
        )
        self.layout.name_text_input = TextInput(
            multiline = False,
            halign = "center",
            padding_y = self.window_height * 0.1 * 0.3
        )
        self.layout.box_for_name_text.add_widget(self.layout.name_text_input)
        self.layout.add_widget(self.layout.box_for_name_text)


        self.layout.box_for_rate_text = GridLayout(
            rows = 1,
            cols = 1,
            pos_hint = {"x": 0.5, "y": 0.375},
            size_hint = (0.4, 0.1)
        )
        self.layout.rate_text_input = TextInput(
            multiline = False,
            halign = "center",
            padding_y = self.window_height * 0.1 * 0.3
        )
        self.layout.box_for_rate_text.add_widget(self.layout.rate_text_input)
        
        self.layout.add_widget(self.layout.box_for_rate_text)


        self.layout.box_for_stock_text = GridLayout(
            rows = 1,
            cols = 1,
            pos_hint = {"x": 0.5, "y": 0.225},
            size_hint = (0.4, 0.1)
        )
        self.layout.stock_text_input = TextInput(
            multiline = False,
            halign = "center",
            padding_y = self.window_height * 0.1 * 0.3
        )
        self.layout.box_for_stock_text.add_widget(self.layout.stock_text_input)
        
        self.layout.add_widget(self.layout.box_for_stock_text)



        # Error Messages

        self.layout.error_no_label = Button(
            text="Item Number Already Exists.", 
            disabled = True,
            disabled_color = red,
            background_color=back_light_grey, 
            size_hint=(0.4, 0.05), 
            pos_hint={"x": 0.5, "y": 0.625},
            background_normal = "",
            
        )
       
        self.layout.error_no_label.background_disabled_normal = self.layout.error_no_label.background_normal

        self.layout.error_invalid_no_label = Button(
            text="Invalid Item Number.", 
            disabled = True,
            disabled_color = red,
            background_color=back_light_grey, 
            size_hint=(0.4, 0.05), 
            pos_hint={"x": 0.5, "y": 0.625},
            background_normal = "",
            
        )
        
        self.layout.error_invalid_no_label.background_disabled_normal = self.layout.error_invalid_no_label.background_normal


        
        self.layout.error_rate_label = Button(
            text="Invalid Prices List.", 
            disabled = True,
            disabled_color = red,
            background_color=back_light_grey, 
            size_hint=(0.4, 0.05), 
            pos_hint={"x": 0.5, "y": 0.325},
            background_normal = "",
        )
        self.layout.error_rate_label.background_disabled_normal = self.layout.error_rate_label.background_normal


        self.layout.error_stock_label = Button(
            text="Invalid Stock Number.", 
            disabled = True,
            disabled_color = red,
            background_color=back_light_grey, 
            size_hint=(0.4, 0.05), 
            pos_hint={"x": 0.5, "y": 0.175},
            background_normal = "",
        )
        self.layout.error_stock_label.background_disabled_normal = self.layout.error_stock_label.background_normal


        self.layout.error_name_label = Button(
            text="Item Name Already Exists.", 
            disabled = True,
            disabled_color = red,
            background_color=back_light_grey, 
            size_hint=(0.4, 0.05), 
            pos_hint={"x": 0.5, "y": 0.475},
            background_normal = "",
        )
        self.layout.error_name_label.background_disabled_normal = self.layout.error_name_label.background_normal


        self.layout.error_rentals_label = Button(
            text="Cannot Edit with Active Rentals", 
            disabled = True,
            disabled_color = red,
            background_color=back_light_grey, 
            size_hint=(0.4, 0.05), 
            pos_hint={"x": 0.1, "y": 0.175},
            background_normal = "",
        )
        self.layout.error_rentals_label.background_disabled_normal = self.layout.error_rentals_label.background_normal




        #Create Buttons

        self.layout.remove_item_btn = Button(
            text="Remove Item", 
            background_color=dark_red, 
            color = (1, 1, 1, 1),
            size_hint=(0.4, 0.05), 
            pos_hint={"x": 0.3, "y": 0.7875},
            background_normal = ""
        )
        self.layout.add_widget(self.layout.remove_item_btn)


        self.layout.cancel_btn = Button(
            text="Cancel", 
            background_color=green, 
            size_hint=(0.5, 0.15), 
            pos_hint={"x": 0, "y": 0},
            background_normal = ""
        )
        self.layout.add_widget(self.layout.cancel_btn)


        self.layout.save_changes_btn = Button(
            text="Save Changes", 
            background_color=green, 
            size_hint=(0.5, 0.15),
            pos_hint={"x": 0.5, "y": 0},
            background_normal = ""
        )
        self.layout.add_widget(self.layout.save_changes_btn)



        # Add layout to Inventory Screen
        self.add_widget(self.layout)


    def update_window_size(self, instance, width, height):
        self.window_width = width 
        self.window_height = height


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

    


    @staticmethod
    def verify_stock_entry(stock):
        try:
            stock = int(stock)
            if stock < 0:
                return False
        except:
            return False 
        
        return True

    

