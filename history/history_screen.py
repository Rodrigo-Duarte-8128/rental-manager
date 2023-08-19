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


class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)

        self.finished_rentals_stored = JsonStore("finished_rentals.json")
        self.row_widgets = {}

        Window.clearcolor = back_light_grey
        self.window_width, self.window_height = Window.size
        Window.bind(on_resize=self.update_window_size)
        
        
        self.layout = FloatLayout()


        # Create Labels
        self.layout.top_label = Button(
            text="Finished Rentals", 
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
        

        self.layout.date_label = Button(
            text = "Date",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            background_color = yellow,
            size_hint = (0.2, 0.1),
            pos_hint = {"x": 0, "y": 0.75},
            background_normal = ""
        )
        self.layout.date_label.background_disabled_normal = self.layout.date_label.background_normal
        self.layout.add_widget(self.layout.date_label)

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
            text = "Total",
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
        date_list = list(self.finished_rentals_stored.keys())
        date_list.sort(key=self.absolute_date, reverse=True)

        for date in date_list:
            simple_date = date.split(".")[0]
            row = RowWidget(
                simple_date,
                self.finished_rentals_stored.get(date)["client_name"],
                self.finished_rentals_stored.get(date)['start_time'],
                f"\u20ac{self.finished_rentals_stored.get(date)['total']}",
            )
            row.date = date
            self.row_widgets[date] = row
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


        self.add_widget(self.layout)


    def update_window_size(self, instance, width, height):
        self.window_width = width 
        self.window_height = height

    
    def absolute_date(self, date):
        ''' 
        returns the amount of time in seconds from january first of the year zero to the given date

        the date must have the form "yyyy-mm-dd hh:mm:ss.mmmm"

        '''
        calendar = {1 : 31, 2 : 28, 3 : 31, 4 : 30, 5 : 31,
            6 : 30, 7 : 31, 8 : 31, 9 : 30, 10 : 31,
            11 : 30, 12 : 31}
        
        leap_calendar = {1 : 31, 2 : 29, 3 : 31, 4 : 30, 5 : 31,
            6 : 30, 7 : 31, 8 : 31, 9 : 30, 10 : 31,
            11 : 30, 12 : 31}
        
        year = int(date[:3])
        month = int(date[5: 7])
        day = int(date[8:10])
        hour = int(date[11:13])
        minutes = int(date[14:16])
        seconds = int(date[17:19])
        miliseconds = int(date.split(".")[1])

        total_days = 0

        for num in range(year):
            total_days += 365 + int(self.is_leap_year(num))

        for mon in range(1, month):
            if not self.is_leap_year(year):
                total_days += calendar[mon]
            else:
                total_days += leap_calendar[mon] 
        total_days += day
        return total_days * 86400 + hour*3600 + minutes*60 + seconds + float(f"0.{miliseconds}")
        
    @staticmethod
    def is_leap_year(year):
    #year is a natural number (incl zero)
        if year % 4 == 0:
            if year % 100 == 0:
                if year % 400 == 0:
                    return True
                return False
            return True
        return False