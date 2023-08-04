from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex as hex
from datetime import datetime


back_light_grey = (211/255,211/255,211/255, 1)
light_grey = hex("#F3F2ED")
green = hex("#01311F")
yellow = hex("#C6AA58")
red = hex("#FF0000")
dark_red = hex("#7f0000")
light_green = hex("#65a765")



class FinishRentalScreen(Screen):
    def __init__(self, inventory_screen, associated_rental, **kwargs):
        super(FinishRentalScreen, self).__init__(**kwargs)

        self.items_rented = list(associated_rental.values())[0]["items_rented"]

        self.start_time = list(associated_rental.values())[0]["start_time"]

        self.end_time = ":".join(datetime.now().strftime("%H:%M:%S").split(":")[:-1])

        self.hourly_price = list(associated_rental.values())[0]["hourly_price"]
        
        
        self.window_width, self.window_height = Window.size
        Window.bind(on_resize=self.update_window_size)

        self.layout = FloatLayout()


        # Create Top Banner
        self.layout.top_label = Button(
            text="Finish Rental", 
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
            size_hint = (0.4, 0.1),
            pos_hint = {"x": 0.1, "y": 0.7},
            background_normal = ""
        )
        self.layout.name_label.background_disabled_normal = self.layout.name_label.background_normal
        self.layout.add_widget(self.layout.name_label)


        self.layout.start_time_label = Button(
            text = "Start Time (HH:MM)",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            background_color = yellow,
            size_hint = (0.4, 0.1),
            pos_hint = {"x": 0.1, "y": 0.55},
            background_normal = ""
        )
        self.layout.start_time_label.background_disabled_normal = self.layout.start_time_label.background_normal
        self.layout.add_widget(self.layout.start_time_label)


        self.layout.end_time_label = Button(
            text = "End Time (HH:MM)",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            background_color = yellow,
            size_hint = (0.4, 0.1),
            pos_hint = {"x": 0.1, "y": 0.4},
            background_normal = ""
        )
        self.layout.end_time_label.background_disabled_normal = self.layout.end_time_label.background_normal
        self.layout.add_widget(self.layout.end_time_label)

        

        self.layout.total_label = Button(
            text = f"TOTAL:    \u20ac {self.total()}",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (0, 0, 0, 1),
            background_color = (1, 1, 1, 1),
            size_hint = (0.5, 0.1),
            pos_hint = {"x": 0.25, "y": 0.25},
            background_normal = ""
        )
        self.layout.total_label.background_disabled_normal = self.layout.total_label.background_normal
        self.layout.add_widget(self.layout.total_label)




        # Create Text Inputs

        self.layout.box_for_name_text = GridLayout(
            rows = 1,
            cols = 1,
            pos_hint = {"x": 0.5, "y": 0.7},
            size_hint = (0.4, 0.1)
        )
        self.layout.name_text_input = TextInput(
            multiline = False,
            halign = "center",
            padding_y = self.window_height * 0.1 * 0.3
        )
        self.layout.box_for_name_text.add_widget(self.layout.name_text_input)
        self.layout.add_widget(self.layout.box_for_name_text)


        self.layout.box_for_hour_text = GridLayout(
            rows = 1,
            cols = 1,
            pos_hint = {"x": 0.5, "y": 0.55},
            size_hint = (0.4, 0.1)
        )
        self.layout.hour_text_input = TextInput(
            multiline = False,
            halign = "center",
            padding_y = self.window_height * 0.1 * 0.3
        )
        self.layout.box_for_hour_text.add_widget(self.layout.hour_text_input)
        self.layout.add_widget(self.layout.box_for_hour_text)

    
        

        self.layout.box_for_end_time_text = GridLayout(
            rows = 1,
            cols = 1,
            pos_hint = {"x": 0.5, "y": 0.4},
            size_hint = (0.4, 0.1)
        )
        self.layout.end_time_text_input = TextInput(
            multiline = False,
            halign = "center",
            padding_y = self.window_height * 0.1 * 0.3
        )
        self.layout.box_for_end_time_text.add_widget(self.layout.end_time_text_input)
        self.layout.add_widget(self.layout.box_for_end_time_text)

        self.layout.end_time_text_input.text = self.end_time






        # Error Messages
        self.layout.error_time_label = Button(
            text="Invalid Time.", 
            disabled = True,
            disabled_color = red,
            background_color=back_light_grey, 
            size_hint=(0.4, 0.05), 
            pos_hint={"x": 0.5, "y": 0.35},
            background_normal = "",
        )
        self.layout.error_time_label.background_disabled_normal = self.layout.error_time_label.background_normal


        self.layout.error_time_label2 = Button(
            text="Invalid Time.", 
            disabled = True,
            disabled_color = red,
            background_color=back_light_grey, 
            size_hint=(0.4, 0.05), 
            pos_hint={"x": 0.5, "y": 0.5},
            background_normal = "",
        )
        self.layout.error_time_label2.background_disabled_normal = self.layout.error_time_label2.background_normal




        #Create Buttons
        self.layout.cancel_btn = Button(
            text="Cancel", 
            background_color=green, 
            size_hint=(0.5, 0.15), 
            pos_hint={"x": 0, "y": 0},
            background_normal = ""
        )
        self.layout.add_widget(self.layout.cancel_btn)


        self.layout.finish_btn = Button(
            text="Finish", 
            background_color=green, 
            size_hint=(0.5, 0.15),
            pos_hint={"x": 0.5, "y": 0},
            background_normal = ""
        )
        self.layout.add_widget(self.layout.finish_btn)


        self.layout.recalculate_btn = Button(
            text="Recalculate", 
            background_color=yellow, 
            color = (1, 1, 1, 1),
            size_hint=(0.3, 0.04), 
            pos_hint={"x": 0.35, "y": 0.175},
            background_normal = ""
        )
        self.layout.add_widget(self.layout.recalculate_btn)


    

        # Add layout to Inventory Screen
        self.add_widget(self.layout)


    def total(self):
        # computes the total amount owed
        # returns float

        absolute_start_time = int(self.start_time.split(":")[0]) * 60 + int(self.start_time.split(":")[1]) 
        absolute_end_time = int(self.end_time.split(":")[0]) * 60 + int(self.end_time.split(":")[1]) 
        time_passed = absolute_end_time - absolute_start_time

        time_passed_in_hours = time_passed / 60

        return round(time_passed_in_hours * float(self.hourly_price.split("\u20ac")[1]), 2)
    



    def recalculate(self, instance):
        
        new_start_time = self.layout.hour_text_input.text
        new_end_time = self.layout.end_time_text_input.text

        
        errors = []

        # validate hour format
        list = new_start_time.split(":")
        try:
            hour = int(list[0])
            minutes = int(list[1])

            if hour < 0 or hour >= 24 or minutes < 0 or minutes >= 60:  
                errors.append("invalid_start_time")
        except:
            errors.append("invalid_start_time")


        list = new_end_time.split(":")
        try:
            hour = int(list[0])
            minutes = int(list[1])

            if hour < 0 or hour >= 24 or minutes < 0 or minutes >= 60:  
                errors.append("invalid_end_time")
        except:
            errors.append("invalid_end_time")
        

        if errors == []:

            absolute_start_time = int(new_start_time.split(":")[0]) * 60 + int(new_start_time.split(":")[1]) 
            absolute_end_time = int(new_end_time.split(":")[0]) * 60 + int(new_end_time.split(":")[1]) 
            time_passed = absolute_end_time - absolute_start_time

            time_passed_in_hours = time_passed / 60

            new_total = round(time_passed_in_hours * float(self.hourly_price.split("\u20ac")[1]), 2)

            self.layout.total_label.text = f"TOTAL:    \u20ac {new_total}"


        if "invalid_start_time" in errors:
            if self.layout.error_time_label2 not in self.layout.children:
                self.layout.add_widget(self.layout.error_time_label2)

    
        if "invalid_start_time" not in errors:
            if self.layout.error_time_label2 in self.layout.children:
                self.layout.remove_widget(self.layout.error_time_label2)

        if "invalid_end_time" in errors:
            if self.layout.error_time_label not in self.layout.children:
                self.layout.add_widget(self.layout.error_time_label)

    
        if "invalid_end_time" not in errors:
            if self.layout.error_time_label in self.layout.children:
                self.layout.remove_widget(self.layout.error_time_label)
        



    def update_window_size(self, instance, width, height):
        self.window_width = width 
        self.window_height = height


