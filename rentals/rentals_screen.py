from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.utils import get_color_from_hex as hex
from kivy.storage.jsonstore import JsonStore
from rentals.rent_row_widget import RowWidget


back_light_grey = (211/255,211/255,211/255, 1)
light_grey = hex("#F3F2ED")
green = hex("#01311F")
yellow = hex("#C6AA58")
red = hex("#FF0000")
dark_red = hex("#7f0000")






class RentalsScreen(Screen):
    def __init__(self, **kwargs):
        super(RentalsScreen, self).__init__(**kwargs)

        self.rentals_stored = JsonStore("active_rentals.json")
        self.row_widgets = {}

        Window.clearcolor = back_light_grey
        self.window_width, self.window_height = Window.size
        Window.bind(on_resize=self.update_window_size)
        
        
        self.layout = FloatLayout()


        

        # Create Labels
        self.layout.top_label = Button(
            text="Active Rentals", 
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
        

        self.layout.id_label = Button(
            text = "No.",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            background_color = yellow,
            size_hint = (0.2, 0.1),
            pos_hint = {"x": 0, "y": 0.75},
            background_normal = ""
        )
        self.layout.id_label.background_disabled_normal = self.layout.id_label.background_normal
        self.layout.add_widget(self.layout.id_label)

        self.layout.name_label = Button(
            text = "Name",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            background_color = yellow,
            size_hint = (0.4, 0.1),
            pos_hint = {"x": 0.2, "y": 0.75},
            background_normal = ""
        )
        self.layout.name_label.background_disabled_normal = self.layout.name_label.background_normal
        self.layout.add_widget(self.layout.name_label)

        self.layout.start_time_label = Button(
            text = "Start Time",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            background_color = yellow,
            size_hint = (0.2, 0.1),
            pos_hint = {"x": 0.6, "y": 0.75},
            background_normal = ""
        )
        self.layout.start_time_label.background_disabled_normal = self.layout.start_time_label.background_normal
        self.layout.add_widget(self.layout.start_time_label)

        self.layout.price_label = Button(
            text = "Price/Hour",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            background_color = yellow,
            size_hint = (0.2, 0.1),
            pos_hint = {"x": 0.8, "y": 0.75},
            background_normal = ""
        )
        self.layout.price_label.background_disabled_normal = self.layout.price_label.background_normal
        self.layout.add_widget(self.layout.price_label)

        


        # Create Grid Layout that holds RentalsView
        self.layout.scroll_layout = GridLayout(
            cols=1,
            size_hint_y=None,
            size = (self.window_width, self.window_height * 0.6),
            row_default_height = 0.1 * self.window_height,
        )
        self.layout.scroll_layout.bind(
            minimum_height=self.layout.scroll_layout.setter("height")
        )
        self.layout.scroll_layout.height = self.layout.scroll_layout.minimum_height



        # Create Rows for the RentalsView
        
        client_id_list = list(map(lambda x: int(x), self.rentals_stored.keys()))
        client_id_list.sort()

        for client_id in client_id_list:
            client_id = str(client_id)
            row = RowWidget(
                client_id,
                self.rentals_stored.get(client_id)["client_name"],
                str(self.rentals_stored[client_id]['start_time']),
                f"\u20ac{self.rentals_stored.get(client_id)['hourly_price']}"
            )
            self.row_widgets[client_id] = row
            self.layout.scroll_layout.add_widget(row)

        
        # Create RentalsView
        self.layout.rentals_view = ScrollView(
            size_hint = (1, 0.6), 
            pos_hint = {"x": 0, "y": 0.15},
            bar_width = 10
        )

        self.layout.rentals_view.add_widget(self.layout.scroll_layout)
        self.layout.add_widget(self.layout.rentals_view)



        

        #Create Buttons
        self.layout.add_rental_btn = Button(
            text="New Rental", 
            background_color=green, 
            size_hint=(0.5, 0.15), 
            pos_hint={"x": 0, "y": 0},
            background_normal = ""
        )
        self.layout.add_widget(self.layout.add_rental_btn)


        self.layout.go_to_inventory_btn = Button(
            text="Inventory", 
            background_color=green, 
            size_hint=(0.5, 0.15),
            pos_hint={"x": 0.5, "y": 0},
            background_normal = ""
        )
        self.layout.add_widget(self.layout.go_to_inventory_btn)


        self.layout.go_to_history_btn = Button(
            text="History", 
            background_color=yellow, 
            size_hint=(0.1, 0.05),
            pos_hint={"x": 0.9, "y": 0.95},
            background_normal = ""
        )
        self.layout.add_widget(self.layout.go_to_history_btn)



        # Add layout to Rental Screen
        self.add_widget(self.layout)


    def update_window_size(self, instance, width, height):
        self.window_width = width 
        self.window_height = height


    
    @staticmethod
    def compute_hourly_price(add_item_screen, items_rented):

        

        no_items_with_daily_rate = True
        for item in items_rented.values():
            if add_item_screen.parse_rate_entry(item["hourly_rate"])[1] != "":
                no_items_with_daily_rate = False

        
        if no_items_with_daily_rate:

            max_no_rates = 0
            for item in items_rented.values():
                no_rates = len(add_item_screen.parse_rate_entry(item["hourly_rate"])[0])
                if  no_rates > max_no_rates:
                    max_no_rates = no_rates

            hourly_prices_list = [[]]
            for hour_rate_no in range(max_no_rates):
                price_for_this_hour = 0
                for item in items_rented.values():
                    parsed_item_rates = add_item_screen.parse_rate_entry(item["hourly_rate"])
                    if hour_rate_no < len(parsed_item_rates[0]):
                        price_for_this_hour += float(parsed_item_rates[0][hour_rate_no]) * float(item["quantity"])
                    else:
                        price_for_this_hour += float(parsed_item_rates[0][-1]) * float(item["quantity"])
                hourly_prices_list[0].append(str(round(price_for_this_hour, 2)))

            hourly_price = ", ".join(hourly_prices_list[0])
            return hourly_price
        

        all_items_with_daily_rate_and_equal_length = True
        st_length = len(add_item_screen.parse_rate_entry(list(items_rented.values())[0]["hourly_rate"])[0])
        for item in items_rented.values():
            if (add_item_screen.parse_rate_entry(item["hourly_rate"])[1] == "" or
                len(add_item_screen.parse_rate_entry(item["hourly_rate"])[0]) != st_length):
                all_items_with_daily_rate_and_equal_length = False


        if all_items_with_daily_rate_and_equal_length:
            hourly_prices_list = [[]]
            for hour_rate_no in range(st_length):
                price_for_this_hour = 0
                for item in items_rented.values():
                    parsed_item_rates = add_item_screen.parse_rate_entry(item["hourly_rate"])
                    price_for_this_hour += float(parsed_item_rates[0][hour_rate_no]) * float(item["quantity"])
                    
                hourly_prices_list[0].append(str(round(price_for_this_hour, 2)))


            total_daily_rate = 0
            for item in items_rented.values():
                total_daily_rate += float(add_item_screen.parse_rate_entry(item["hourly_rate"])[1]) * float(item["quantity"])

            hourly_prices_list.append(str(round(total_daily_rate, 2)))
            hourly_price = ", ".join(hourly_prices_list[0])
            hourly_price += f" - {hourly_prices_list[1]}"
            return hourly_price
        
        
        for item in items_rented.values():
            parsed = add_item_screen.parse_rate_entry(item["hourly_rate"])
            if parsed[1] != "":
                min_len_item_with_daily_rate = len(parsed[0])
                break

        for item in items_rented.values():
            parsed = add_item_screen.parse_rate_entry(item["hourly_rate"])
            length = len(parsed[0])
            if parsed[1] != "" and length < min_len_item_with_daily_rate:
                min_len_item_with_daily_rate = length
        

        hourly_prices_list = [[]]
        for hour_rate_no in range(min_len_item_with_daily_rate):
            price_for_this_hour = 0
           
            for item in items_rented.values():
                parsed_item_rates = add_item_screen.parse_rate_entry(item["hourly_rate"])
                if hour_rate_no < len(parsed_item_rates[0]):
                    price_for_this_hour += float(parsed_item_rates[0][hour_rate_no]) * float(item["quantity"])
                else:
                    price_for_this_hour += float(parsed_item_rates[0][-1]) * float(item["quantity"])

            hourly_prices_list[0].append(str(round(price_for_this_hour, 2)))
        
        hourly_price = ", ".join(hourly_prices_list[0])
        hourly_price += " - ?"
        return hourly_price
           
       




        

