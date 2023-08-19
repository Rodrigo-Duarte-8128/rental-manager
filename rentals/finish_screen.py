from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.utils import get_color_from_hex as hex
from datetime import datetime
from rentals.add_rental_row_widget import AddRentalRowWidget


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

        self.associated_rental = associated_rental
        
        
        self.window_width, self.window_height = Window.size
        Window.bind(on_resize=self.update_window_size)

        self.row_widgets = {}
        self.layout = FloatLayout()


        # Create Grid Layout that will Scroll
        self.layout.scroll_layout = GridLayout(
            cols=1,
            size_hint_y=None,
            size = (self.window_width, self.window_height * 0.255),
            row_default_height = 0.1 * self.window_height,
        )
        self.layout.scroll_layout.bind(
            minimum_height=self.layout.scroll_layout.setter("height")
        )
        self.layout.scroll_layout.height = self.layout.scroll_layout.minimum_height



        # Create Rows for the ItemsView
        
        item_no_list = list(map(lambda x: int(x), self.items_rented.keys()))
        item_no_list.sort()

        for item_no in item_no_list:
            item_no = str(item_no)
            row = AddRentalRowWidget(
                item_no,
                inventory_screen.items_stored.get(item_no)["item_name"],
                f"\u20ac{inventory_screen.items_stored.get(item_no)['hourly_rate']}",
                str(self.items_rented[item_no]["quantity"]),
                self.window_height, 
            )
            self.row_widgets[item_no] = row
            self.layout.scroll_layout.add_widget(row)

        
        # Create ItemsView
        self.layout.items_view = ScrollView(
            size_hint = (1, 0.26), 
            pos_hint = {"x": 0, "y": 0.285},
            bar_width = 10
        )

        self.layout.items_view.add_widget(self.layout.scroll_layout)
        self.layout.add_widget(self.layout.items_view)



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
            size_hint = (0.4, 0.075),
            pos_hint = {"x": 0.1, "y": 0.765},
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
            size_hint = (0.4, 0.075),
            pos_hint = {"x": 0.1, "y": 0.68},
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
            size_hint = (0.4, 0.075),
            pos_hint = {"x": 0.1, "y": 0.595},
            background_normal = ""
        )
        self.layout.end_time_label.background_disabled_normal = self.layout.end_time_label.background_normal
        self.layout.add_widget(self.layout.end_time_label)

        self.layout.choose_items_label = Button(
            text = "Quantity to Finish",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (0, 0, 0, 1),
            background_color = back_light_grey,
            size_hint = (0.15, 0.025),
            pos_hint = {"x": 0.15, "y": 0.56},
            background_normal = ""
        )
        self.layout.choose_items_label.background_disabled_normal = self.layout.choose_items_label.background_normal
        self.layout.add_widget(self.layout.choose_items_label)

        

        self.layout.total_label = Button(
            text = f"SUBTOTAL:    \u20ac {self.subtotal(self.start_time, self.end_time)}\n       TOTAL:    \u20ac {self.total(self.start_time, self.end_time)}",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (0, 0, 0, 1),
            background_color = (1, 1, 1, 1),
            size_hint = (0.5, 0.075),
            pos_hint = {"x": 0.25, "y": 0.2},
            background_normal = ""
        )
        self.layout.total_label.background_disabled_normal = self.layout.total_label.background_normal
        self.layout.add_widget(self.layout.total_label)




        
       


        # Create Text Inputs

        self.layout.box_for_name_text = GridLayout(
            rows = 1,
            cols = 1,
            pos_hint = {"x": 0.5, "y": 0.765},
            size_hint = (0.4, 0.075)
        )
        self.layout.name_text_input = TextInput(
            multiline = False,
            halign = "center",
            padding_y = self.window_height * 0.075 * 0.3
        )
        self.layout.box_for_name_text.add_widget(self.layout.name_text_input)
        self.layout.add_widget(self.layout.box_for_name_text)


        self.layout.box_for_hour_text = GridLayout(
            rows = 1,
            cols = 1,
            pos_hint = {"x": 0.5, "y": 0.68},
            size_hint = (0.4, 0.075)
        )
        self.layout.hour_text_input = TextInput(
            multiline = False,
            halign = "center",
            padding_y = self.window_height * 0.075 * 0.3
        )
        self.layout.box_for_hour_text.add_widget(self.layout.hour_text_input)
        self.layout.add_widget(self.layout.box_for_hour_text)

    
        

        self.layout.box_for_end_time_text = GridLayout(
            rows = 1,
            cols = 1,
            pos_hint = {"x": 0.5, "y": 0.595},
            size_hint = (0.4, 0.075)
        )
        self.layout.end_time_text_input = TextInput(
            multiline = False,
            halign = "center",
            padding_y = self.window_height * 0.075 * 0.3
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
            size_hint=(0.4, 0.025), 
            pos_hint={"x": 0.5, "y": 0.56},
            background_normal = "",
        )
        self.layout.error_time_label.background_disabled_normal = self.layout.error_time_label.background_normal
        

        


        self.layout.error_quantity_label = Button(
            text="Invalid Quantity.", 
            disabled = True,
            disabled_color = red,
            background_color=back_light_grey, 
            size_hint=(0.25, 0.075), 
            pos_hint={"x": 0, "y": 0.2},
            background_normal = "",
        )
        self.layout.error_quantity_label.background_disabled_normal = self.layout.error_quantity_label.background_normal
        

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
            pos_hint={"x": 0.35, "y": 0.155},
            background_normal = ""
        )
        self.layout.add_widget(self.layout.recalculate_btn)


    

        # Add layout to Inventory Screen
        self.add_widget(self.layout)



    def total(self, start_time, end_time):
        rental = list(self.associated_rental.values())[0]
        previous_subtotals = rental.get("subtotal", 0)
        previous_subtotals = float(previous_subtotals)     
        current_subtotal = self.subtotal(start_time, end_time)

        return round(previous_subtotals + current_subtotal, 2)


    def subtotal(self, start_time, end_time):
        # computes the total amount owed
        # returns float
 

        absolute_start_time = int(start_time.split(":")[0]) * 60 + int(start_time.split(":")[1]) 
        absolute_end_time = int(end_time.split(":")[0]) * 60 + int(end_time.split(":")[1]) 
        time_passed = absolute_end_time - absolute_start_time

        time_passed_in_hours = time_passed / 60

        total = 0
        max_int_hour = int(time_passed_in_hours)
        # take into account the full hours that the items were rented
        hour = 1 
        while hour <= max_int_hour:
            hour_total = 0
            for item_no, item in self.items_rented.items():
                parsed_rate = self.parse_rate_string(item["hourly_rate"])
                
                quantity_to_finish = self.row_widgets[item_no].quantity_text_input.text
                                        
                if quantity_to_finish == "":
                    continue
                else:
                    quantity_to_finish = int(quantity_to_finish)
                    if parsed_rate[1] == "":
                        if hour <= len(parsed_rate[0]):
                            hour_total += float(parsed_rate[0][hour - 1]) * quantity_to_finish
                        else:
                            hour_total += float(parsed_rate[0][-1]) * quantity_to_finish
                    else:   # if an item has a daily rate we should only add the hourly rates if the total time does not exceed
                            # the amount of time for the daily rate to kick in
                        if max_int_hour < len(parsed_rate[0]) or (max_int_hour == len(parsed_rate[0]) and time_passed_in_hours == float(max_int_hour)):
                            hour_total += float(parsed_rate[0][hour-1]) * quantity_to_finish

            total += hour_total
            hour += 1
        
        
        # take into account the fractional hours that the items were rented for
        for item_no, item in self.items_rented.items():
            parsed_rate = self.parse_rate_string(item["hourly_rate"]) 
            quantity_to_finish = self.row_widgets[item_no].quantity_text_input.text
            
            if quantity_to_finish == "":
                continue
            else:
                quantity_to_finish = int(quantity_to_finish)
                if parsed_rate[1] == "":
                    if max_int_hour < len(parsed_rate[0]):
                        total += (time_passed_in_hours - max_int_hour) * float(parsed_rate[0][max_int_hour]) * quantity_to_finish
                    else:
                        total += (time_passed_in_hours - max_int_hour) * float(parsed_rate[0][-1]) * quantity_to_finish
                else:
                    if max_int_hour < len(parsed_rate[0]):
                        total += (time_passed_in_hours - max_int_hour) * float(parsed_rate[0][max_int_hour]) * quantity_to_finish
                    
        

            
        
        # take into account the items with daily rate that were activated
        for item_no, item in self.items_rented.items():
            parsed_rate = self.parse_rate_string(item["hourly_rate"])
            quantity_to_finish = self.row_widgets[item_no].quantity_text_input.text

            if quantity_to_finish == "":
                continue
            else:
                quantity_to_finish = int(quantity_to_finish)
                if parsed_rate[1] != "" and time_passed_in_hours > len(parsed_rate[0]):
                    total += float(parsed_rate[1]) * quantity_to_finish
        

        return round(total, 2)
    
    


    
    def parse_rate_string(self, hourly_rate):
        # if the rate looks like "1, 2, 3" returns [["1", "2", "3"], ""]
        # if the rate looks like "1, 2 - 3" returns [["1", "2"], "3"]
        
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
    


    



    def recalculate(self, inventory_screen):
        
        def do(instance):
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
            

            # validate quantities to finish
            for item_no, row_widget in self.row_widgets.items():
                quantity_to_finish = row_widget.quantity_text_input.text

                if quantity_to_finish == "":
                    continue
                else:
                    total_quantity = int(row_widget.stock)
                    try:
                        int_quantity_to_finish = int(quantity_to_finish)
                        if int_quantity_to_finish <= 0:
                            errors.append("invalid_quantity")

                        if int_quantity_to_finish > int(total_quantity):
                            errors.append("invalid_quantity")

                    except:
                        errors.append("invalid_quantity")

            if errors == []:


                new_subtotal = self.subtotal(new_start_time, new_end_time)
                new_total = self.total(new_start_time, new_end_time)
                self.layout.total_label.text = f"SUBTOTAL:    \u20ac {new_subtotal}\n       TOTAL:    \u20ac {new_total}"


            if "invalid_start_time" in errors or "invalid_end_time" in errors:
                if self.layout.error_time_label not in self.layout.children:
                    self.layout.add_widget(self.layout.error_time_label)

        
            if "invalid_start_time" not in errors and "invalid_end_time" not in errors:
                if self.layout.error_time_label in self.layout.children:
                    self.layout.remove_widget(self.layout.error_time_label)

            if "invalid_quantity" in errors:
                if self.layout.error_quantity_label not in self.layout.children:
                    self.layout.add_widget(self.layout.error_quantity_label)

        
            if "invalid_quantity" not in errors:
                if self.layout.error_quantity_label in self.layout.children:
                    self.layout.remove_widget(self.layout.error_quantity_label)

        
        return do


    def update_window_size(self, instance, width, height):
        self.window_width = width 
        self.window_height = height


