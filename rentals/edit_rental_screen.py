from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex as hex
from datetime import datetime
from inventory.inv_row_widget import RowWidget as InvRowWidget


back_light_grey = (211/255,211/255,211/255, 1)
light_grey = hex("#F3F2ED")
green = hex("#01311F")
yellow = hex("#C6AA58")
red = hex("#FF0000")
dark_red = hex("#7f0000")
light_green = hex("#65a765")



class EditRentalScreen(Screen):
    def __init__(self, inventory_screen, associated_rental, **kwargs):
        super(EditRentalScreen, self).__init__(**kwargs)

        self.items_rented = list(associated_rental.values())[0]["items_rented"] # original list
        self.items_to_rent = list(associated_rental.values())[0]["items_rented"].copy() # new list
        self.row_widgets = {}

        self.window_width, self.window_height = Window.size
        Window.bind(on_resize=self.update_window_size)

        self.layout = FloatLayout()


        # Create Top Banner
        self.layout.top_label = Button(
            text="Edit Rental", 
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
            text = "New Name",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            background_color = yellow,
            size_hint = (0.4, 0.09),
            pos_hint = {"x": 0.1, "y": 0.705},
            background_normal = ""
        )
        self.layout.name_label.background_disabled_normal = self.layout.name_label.background_normal
        self.layout.add_widget(self.layout.name_label)


        self.layout.start_time_label = Button(
            text = "New Start Time (HH:MM)",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            background_color = yellow,
            size_hint = (0.4, 0.09),
            pos_hint = {"x": 0.1, "y": 0.61},
            background_normal = ""
        )
        self.layout.start_time_label.background_disabled_normal = self.layout.start_time_label.background_normal
        self.layout.add_widget(self.layout.start_time_label)

        


        self.layout.choose_items_label = Button(
            text = "Choose Items",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (0, 0, 0, 1),
            background_color = back_light_grey,
            size_hint = (0.4, 0.05),
            pos_hint = {"x": 0.1, "y": 0.56},
            background_normal = ""
        )
        self.layout.choose_items_label.background_disabled_normal = self.layout.choose_items_label.background_normal
        self.layout.add_widget(self.layout.choose_items_label)


        self.layout.added_label = Button(
            text = "Added",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            background_color = yellow,
            size_hint = (0.2, 0.05),
            pos_hint = {"x": 0, "y": 0.2},
            background_normal = ""
        )
        self.layout.added_label.background_disabled_normal = self.layout.added_label.background_normal
        self.layout.add_widget(self.layout.added_label)


        self.layout.added_items_label = Button(
            text = "",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (0, 0, 0, 1),
            background_color = (1, 1, 1, 1),
            size_hint = (0.8, 0.05),
            pos_hint = {"x": 0.2, "y": 0.2},
            background_normal = ""
        )
        self.layout.added_items_label.background_disabled_normal = self.layout.added_items_label.background_normal
        self.layout.add_widget(self.layout.added_items_label)

        new_string = ""
        no_list = list(map(lambda x: int(x), list(self.items_rented.keys())))
        no_list.sort()
                    
        for idx, item_no in enumerate(no_list):
            if idx == 0:
                new_string += str(item_no)
            else:
                new_string += f", {item_no}"

        self.layout.added_items_label.text = new_string


        self.layout.info_label = Button(
            text = "Click Again to Remove",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (0, 0, 0, 1),
            background_color = back_light_grey,
            size_hint = (0.5, 0.05),
            pos_hint = {"x": 0, "y": 0.15},
            background_normal = ""
        )
        self.layout.info_label.background_disabled_normal = self.layout.info_label.background_normal
        self.layout.add_widget(self.layout.info_label)




        # Create Text Inputs

        self.layout.box_for_name_text = GridLayout(
            rows = 1,
            cols = 1,
            pos_hint = {"x": 0.5, "y": 0.705},
            size_hint = (0.4, 0.09)
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
            pos_hint = {"x": 0.5, "y": 0.61},
            size_hint = (0.4, 0.09)
        )
        self.layout.hour_text_input = TextInput(
            multiline = False,
            halign = "center",
            padding_y = self.window_height * 0.1 * 0.3
        )
        self.layout.box_for_hour_text.add_widget(self.layout.hour_text_input)
        self.layout.add_widget(self.layout.box_for_hour_text)

        self.layout.hour_text_input.text = ":".join(datetime.now().strftime("%H:%M:%S").split(":")[:-1])
        




        # Create Grid Layout that will Scroll
        self.layout.scroll_layout = GridLayout(
            cols=1,
            size_hint_y=None,
            size = (self.window_width, self.window_height * 0.325),
            row_default_height = 0.1 * self.window_height,
        )
        self.layout.scroll_layout.bind(
            minimum_height=self.layout.scroll_layout.setter("height")
        )
        self.layout.scroll_layout.height = self.layout.scroll_layout.minimum_height



        # Create Rows for the ItemsView
        

        item_no_list = list(map(lambda x: int(x), inventory_screen.items_stored.keys()))
        item_no_list.sort()

        for item_no in item_no_list:
            item_no = str(item_no)
            row = InvRowWidget(
                item_no,
                inventory_screen.items_stored.get(item_no)["item_name"],
                f"\u20ac{inventory_screen.items_stored.get(item_no)['hourly_rate']}",
                str(inventory_screen.items_stored[item_no]['stock'])
            )
            self.row_widgets[item_no] = row
            self.layout.scroll_layout.add_widget(row)

        
        # Create ItemsView
        self.layout.items_view = ScrollView(
            size_hint = (1, 0.325), 
            pos_hint = {"x": 0, "y": 0.25},
            bar_width = 10
        )

        self.layout.items_view.add_widget(self.layout.scroll_layout)
        self.layout.add_widget(self.layout.items_view)



        # Error Messages
        self.layout.error_time_label = Button(
            text="Invalid Time.", 
            disabled = True,
            disabled_color = red,
            background_color=back_light_grey, 
            size_hint=(0.4, 0.05), 
            pos_hint={"x": 0.5, "y": 0.56},
            background_normal = "",
        )
        self.layout.error_time_label.background_disabled_normal = self.layout.error_time_label.background_normal


        self.layout.error_items_label = Button(
            text="No Items Added.", 
            disabled = True,
            disabled_color = red,
            background_color=back_light_grey, 
            size_hint=(0.4, 0.05), 
            pos_hint={"x": 0.5, "y": 0.15},
            background_normal = "",
        )
        self.layout.error_items_label.background_disabled_normal = self.layout.error_items_label.background_normal




        #Create Buttons
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


        self.layout.remove_rental_btn = Button(
            text="Remove", 
            background_color=dark_red, 
            color = (1, 1, 1, 1),
            size_hint=(0.3, 0.04), 
            pos_hint={"x": 0.15, "y": 0.805},
            background_normal = ""
        )
        self.layout.add_widget(self.layout.remove_rental_btn)


        self.layout.finish_rental_btn = Button(
            text="Finish", 
            background_color=light_green, 
            color = (1, 1, 1, 1),
            size_hint=(0.3, 0.04), 
            pos_hint={"x": 0.55, "y": 0.805},
            background_normal = ""
        )
        self.layout.add_widget(self.layout.finish_rental_btn)



        # Add layout to Inventory Screen
        self.add_widget(self.layout)




    def update_window_size(self, instance, width, height):
        self.window_width = width 
        self.window_height = height
