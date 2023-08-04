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



        # Add layout to Rental Screen
        self.add_widget(self.layout)


    def update_window_size(self, instance, width, height):
        self.window_width = width 
        self.window_height = height


    








        

