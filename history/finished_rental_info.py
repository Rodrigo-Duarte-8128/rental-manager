
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from inventory.inv_row_widget import RowWidget 



back_light_grey = (211/255,211/255,211/255, 1)
light_grey = hex("#F3F2ED")
green = hex("#01311F")
yellow = hex("#C6AA58")
red = hex("#FF0000")
dark_red = hex("#7f0000")


class FinishedRentalScreen(Screen):
    def __init__(self, date, history_screen, **kwargs):
        super(FinishedRentalScreen, self).__init__(**kwargs)

        

        self.window_width, self.window_height = Window.size
        Window.bind(on_resize=self.update_window_size)

        self.row_widgets = {}

        self.layout = FloatLayout()


        # Create Top Banner
        self.layout.top_label = Button(
            text="Finished Rental Info", 
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
        
        item_no_list = list(map(lambda x: int(x), history_screen.finished_rentals_stored.get(date)["items_finished"].keys()))
        item_no_list.sort()

        for item_no in item_no_list:
            item_no = str(item_no)
            item = history_screen.finished_rentals_stored.get(date)["items_finished"][item_no]
            row = RowWidget(
                item_no,
                item["item_name"],
                f"\u20ac{item['hourly_rate']}",
                str(item["quantity_to_finish"]),
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



        # Create Labels
        self.layout.name_label = Button(
            text = "Name",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            background_color = yellow,
            size_hint = (0.4, 0.075),
            pos_hint = {"x": 0.1, "y": 0.715},
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
            size_hint = (0.4, 0.075),
            pos_hint = {"x": 0.1, "y": 0.63},
            background_normal = ""
        )
        self.layout.start_time_label.background_disabled_normal = self.layout.start_time_label.background_normal
        self.layout.add_widget(self.layout.start_time_label)


        self.layout.end_time_label = Button(
            text = "End Time",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            background_color = yellow,
            size_hint = (0.4, 0.075),
            pos_hint = {"x": 0.1, "y": 0.545},
            background_normal = ""
        )
        self.layout.end_time_label.background_disabled_normal = self.layout.end_time_label.background_normal
        self.layout.add_widget(self.layout.end_time_label)


        self.layout.total_label = Button(
            text = f"TOTAL:    \u20ac {history_screen.finished_rentals_stored.get(date)['total']}",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (0, 0, 0, 1),
            background_color = (1, 1, 1, 1),
            size_hint = (0.5, 0.075),
            pos_hint = {"x": 0.25, "y": 0.16},
            background_normal = ""
        )
        self.layout.total_label.background_disabled_normal = self.layout.total_label.background_normal
        self.layout.add_widget(self.layout.total_label)




        # Create Text Inputs
        self.layout.box_for_name_text = GridLayout(
            rows = 1,
            cols = 1,
            pos_hint = {"x": 0.5, "y": 0.715},
            size_hint = (0.4, 0.075)
        )
        self.layout.name_text_input = TextInput(
            multiline = False,
            halign = "center",
            padding_y = self.window_height * 0.075 * 0.3
        )
        self.layout.box_for_name_text.add_widget(self.layout.name_text_input)
        self.layout.add_widget(self.layout.box_for_name_text)



        self.layout.box_for_start_time_text = GridLayout(
            rows = 1,
            cols = 1,
            pos_hint = {"x": 0.5, "y": 0.63}, 
            size_hint = (0.4, 0.075)
        )
        self.layout.start_time_text_input = TextInput(
            multiline = False,
            halign = "center",
            padding_y = self.window_height * 0.075 * 0.3
        )
        self.layout.box_for_start_time_text.add_widget(self.layout.start_time_text_input)
        self.layout.add_widget(self.layout.box_for_start_time_text)


        self.layout.box_for_end_time_text = GridLayout(
            rows = 1,
            cols = 1,
            pos_hint = {"x": 0.5, "y": 0.545},
            size_hint = (0.4, 0.075)
        )
        self.layout.end_time_text_input = TextInput(
            multiline = False,
            halign = "center",
            padding_y = self.window_height * 0.075 * 0.3
        )
        self.layout.box_for_end_time_text.add_widget(self.layout.end_time_text_input)

        self.layout.add_widget(self.layout.box_for_end_time_text)


        



        #Create Buttons
        self.layout.remove_finished_rental_btn = Button(
            text="Remove Finished Rental", 
            background_color=dark_red, 
            color = (1, 1, 1, 1),
            size_hint=(0.4, 0.04), 
            pos_hint={"x": 0.3, "y": 0.805},
            background_normal = ""
        )
        self.layout.add_widget(self.layout.remove_finished_rental_btn)


        self.layout.go_back_btn = Button(
            text="Back", 
            background_color=green, 
            size_hint=(0.5, 0.15), 
            pos_hint={"x": 0, "y": 0},
            background_normal = ""
        )
        self.layout.add_widget(self.layout.go_back_btn)

        self.layout.empty_btn = Button(
            text="", 
            background_color=green, 
            size_hint=(0.5, 0.15), 
            pos_hint={"x": 0.5, "y": 0},
            background_normal = ""
        )
        self.layout.add_widget(self.layout.empty_btn)
        

        # Add layout to Inventory Screen
        self.add_widget(self.layout)



    def update_window_size(self, instance, width, height):
        self.window_width = width 
        self.window_height = height