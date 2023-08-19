from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex as hex



back_light_grey = (211/255,211/255,211/255, 1)
light_grey = hex("#F3F2ED")
green = hex("#01311F")
yellow = hex("#C6AA58")
red = hex("#FF0000")
dark_red = hex("#7f0000")


class AddRentalRowWidget(FloatLayout):
    def __init__(self, item_no, item_name, hourly_rate, stock, window_height, **kwargs):
        super(AddRentalRowWidget, self).__init__(**kwargs)
    
        self.item_no = item_no
        self.item_name = item_name 
        self.hourly_rate = hourly_rate 
        self.stock = stock 
        self.window_height = window_height


        self.size_hint_y = None


        self.no_label = Button(
            text = self.item_no,
            disabled = True,
            disabled_color = (0, 0, 0, 1),
            background_color = light_grey,
            size_hint = (0.15, 0.9),
            pos_hint = {"x": 0, "y": 0},
            background_normal = "",
            
        )
        self.no_label.background_disabled_normal = self.no_label.background_normal
        self.add_widget(self.no_label)


        self.box_for_quantity_text = GridLayout(
            rows = 1,
            cols = 1,
            pos_hint = {"x": 0.15, "y": 0},
            size_hint = (0.15, 0.9)
        )
        self.quantity_text_input = TextInput(
            multiline = False,
            halign = "center",
            padding_y = self.window_height * 0.2 * 0.3
        )
        self.box_for_quantity_text.add_widget(self.quantity_text_input)
        self.add_widget(self.box_for_quantity_text)



        self.item_name_btn= Button(
            text=self.item_name, 
            disabled = True,
            disabled_color = (0, 0, 0, 1),
            background_color=light_grey, 
            size_hint=(0.3, 0.9), 
            pos_hint={"x": 0.3, "y": 0},
            background_normal = "",
        )
        self.item_name_btn.background_disabled_normal = self.item_name_btn.background_normal
        self.add_widget(self.item_name_btn)


        self.hourly_rate_label = Button(
            text = self.hourly_rate,
            disabled = True,
            disabled_color = (0, 0, 0, 1),
            background_color = light_grey,
            size_hint = (0.2, 0.9),
            pos_hint = {"x": 0.6, "y": 0},
            background_normal = "",
            
        )
        self.hourly_rate_label.background_disabled_normal = self.hourly_rate_label.background_normal
        self.add_widget(self.hourly_rate_label)


        self.stock_label = Button(
            text = self.stock,
            disabled = True,
            disabled_color = (0, 0, 0, 1),
            background_color = light_grey,
            size_hint = (0.2, 0.9),
            pos_hint = {"x": 0.8, "y": 0},
            background_normal = "",
            
        )
        self.stock_label.background_disabled_normal = self.stock_label.background_normal
        self.add_widget(self.stock_label)