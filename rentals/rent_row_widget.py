from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.utils import get_color_from_hex as hex



back_light_grey = (211/255,211/255,211/255, 1)
light_grey = hex("#F3F2ED")
green = hex("#01311F")
yellow = hex("#C6AA58")
red = hex("#FF0000")
dark_red = hex("#7f0000")


class RowWidget(FloatLayout):
    def __init__(self, client_id, client_name, start_time, hourly_price, **kwargs):
        super(RowWidget, self).__init__(**kwargs)
    
        self.client_id = client_id 
        self.client_name = client_name 
        self.start_time = start_time 
        self.hourly_price = hourly_price 

        self.size_hint_y = None


        self.id_label = Button(
            text = self.client_id,
            disabled = True,
            disabled_color = (0, 0, 0, 1),
            background_color = light_grey,
            size_hint = (0.2, 0.9),
            pos_hint = {"x": 0, "y": 0},
            background_normal = "",
            
        )
        self.id_label.background_disabled_normal = self.id_label.background_normal
        self.add_widget(self.id_label)


        self.client_name_btn = Button(
            text=self.client_name, 
            color = (0, 0, 0, 1),
            background_color=light_grey, 
            size_hint=(0.4, 0.9), 
            pos_hint={"x": 0.2, "y": 0},
            background_normal = "",
            
            
        )
        self.add_widget(self.client_name_btn)


        self.start_time_label = Button(
            text = self.start_time,
            disabled = True,
            disabled_color = (0, 0, 0, 1),
            background_color = light_grey,
            size_hint = (0.2, 0.9),
            pos_hint = {"x": 0.6, "y": 0},
            background_normal = "",
            
        )
        self.start_time_label.background_disabled_normal = self.start_time_label.background_normal
        self.add_widget(self.start_time_label)


        self.hourly_price_label = Button(
            text = self.hourly_price,
            disabled = True,
            disabled_color = (0, 0, 0, 1),
            background_color = light_grey,
            size_hint = (0.2, 0.9),
            pos_hint = {"x": 0.8, "y": 0},
            background_normal = "",
            
        )
        self.hourly_price_label.background_disabled_normal = self.hourly_price_label.background_normal
        self.add_widget(self.hourly_price_label)