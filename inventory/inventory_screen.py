
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivy.storage.jsonstore import JsonStore
from inventory.inv_row_widget import RowWidget


back_light_grey = (211/255,211/255,211/255, 1)
light_grey = hex("#F3F2ED")
green = hex("#01311F")
yellow = hex("#C6AA58")
red = hex("#FF0000")
dark_red = hex("#7f0000")





class InventoryScreen(Screen):

    def __init__(self, **kwargs):
        super(InventoryScreen, self).__init__(**kwargs)

        self.items_stored = JsonStore("inventory_items.json")


        
        self.window_width, self.window_height = Window.size
        Window.bind(on_resize=self.update_window_size)

        self.layout = FloatLayout()


        # Create Top Banner
        self.layout.top_label = Button(
            text="Inventory Items", 
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
        self.layout.no_label = Button(
            text = "No.",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            background_color = yellow,
            size_hint = (0.2, 0.1),
            pos_hint = {"x": 0, "y": 0.75},
            background_normal = ""
        )
        self.layout.no_label.background_disabled_normal = self.layout.no_label.background_normal
        self.layout.add_widget(self.layout.no_label)

        self.layout.name_label = Button(
            text = "Item Name",
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

        self.layout.hourly_rate_label = Button(
            text = "Prices",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            background_color = yellow,
            size_hint = (0.2, 0.1),
            pos_hint = {"x": 0.6, "y": 0.75},
            background_normal = ""
        )
        self.layout.hourly_rate_label.background_disabled_normal = self.layout.hourly_rate_label.background_normal
        self.layout.add_widget(self.layout.hourly_rate_label)

        self.layout.stock_label = Button(
            text = "Stock",
            color = (1, 1, 1, 1),
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            background_color = yellow,
            size_hint = (0.2, 0.1),
            pos_hint = {"x": 0.8, "y": 0.75},
            background_normal = ""
        )
        self.layout.stock_label.background_disabled_normal = self.layout.stock_label.background_normal
        self.layout.add_widget(self.layout.stock_label)


        # Create Grid Layout that will Scroll
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



        # Create Rows for the ItemsView 
        self.row_widgets = {}

        item_no_list = list(map(lambda x: int(x), self.items_stored.keys()))
        item_no_list.sort()

        for item_no in item_no_list:
            item_no = str(item_no)
            row = RowWidget(
                item_no,
                self.items_stored.get(item_no)["item_name"],
                f"\u20ac{self.items_stored.get(item_no)['hourly_rate']}",
                str(self.items_stored[item_no]['stock'])
            )
            self.row_widgets[item_no] = row
            self.layout.scroll_layout.add_widget(row)

        
        # Create ItemsView
        self.layout.items_view = ScrollView(
            size_hint = (1, 0.6), 
            pos_hint = {"x": 0, "y": 0.15},
            bar_width = 10
        )

        self.layout.items_view.add_widget(self.layout.scroll_layout)
        self.layout.add_widget(self.layout.items_view)


        #Create Buttons
        self.layout.go_to_rentals_btn = Button(
            text="Rentals", 
            background_color=green, 
            size_hint=(0.5, 0.15), 
            pos_hint={"x": 0, "y": 0},
            background_normal = ""
        )
        self.layout.add_widget(self.layout.go_to_rentals_btn)


        self.layout.add_item_btn = Button(
            text="Add Item", 
            background_color=green, 
            size_hint=(0.5, 0.15),
            pos_hint={"x": 0.5, "y": 0},
            background_normal = ""
        )
        self.layout.add_widget(self.layout.add_item_btn)



        # Add layout to Inventory Screen
        self.add_widget(self.layout)


    def update_window_size(self, instance, width, height):
        self.window_width = width 
        self.window_height = height

    
    def add_item(self, item_name, hourly_rate, stock, add_item_screen, add_rental_screen):
        this_item_no = None
        max_item_no = 0
        error = [] 
        
        for item_no in self.items_stored.keys():
            if int(item_no) > max_item_no:
                max_item_no = int(item_no)
            
            if self.items_stored.get(item_no)["item_name"] == item_name:
                if add_item_screen.layout.error_add_label not in add_item_screen.layout.children:
                    add_item_screen.layout.add_widget(add_item_screen.layout.error_add_label)
                error.append("invalid_name")
                break


        
        if not add_item_screen.verify_rate_entry(hourly_rate):
            error.append("invalid_rate")
        
        # try:
        #     rate = float(add_item_screen.layout.rate_text_input.text)
        #     if rate < 0:
        #         error.append("invalid_rate")
        # except:
        #     error.append("invalid_rate")

        if not add_item_screen.verify_stock_entry(stock):
            error.append("invalid_stock")

        # try:
        #     stock_int = int(add_item_screen.layout.stock_text_input.text)
        #     if stock_int < 0:
        #         error.append("invalid_stock")
        # except:
        #     error.append("invalid_stock")
        

        if error == []:

            if add_item_screen.layout.error_add_label in add_item_screen.layout.children:
                add_item_screen.layout.remove_widget(add_item_screen.layout.error_add_label)

            this_item_no = max_item_no + 1

            self.items_stored.put(str(this_item_no),item_name=item_name, hourly_rate=hourly_rate, stock=stock)

            new_row = RowWidget(
                    str(this_item_no),
                    item_name,
                    f"\u20ac{hourly_rate}",
                    stock
                )
            self.layout.scroll_layout.add_widget(new_row)
            self.row_widgets[str(this_item_no)] = new_row

            new_row2 = RowWidget(
                    str(this_item_no),
                    item_name,
                    f"\u20ac{hourly_rate}",
                    stock
                )

            add_rental_screen.layout.scroll_layout.add_widget(new_row2)
            add_rental_screen.row_widgets[str(this_item_no)] = new_row2

        return str(this_item_no), error


        
    
    def remove_item(self, item_no):

        if self.items_stored.exists(item_no):
            self.items_stored.delete(item_no)
            del self.row_widgets[item_no]

        else:
            raise ValueError("Item doesn't exist.")



if __name__ == "__main__":
    pass
    
